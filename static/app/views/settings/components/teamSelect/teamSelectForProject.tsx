import React from 'react';
import styled from '@emotion/styled';

import {Button} from 'sentry/components/button';
import Confirm from 'sentry/components/confirm';
import EmptyMessage from 'sentry/components/emptyMessage';
import {TeamBadge} from 'sentry/components/idBadge/teamBadge';
import Link from 'sentry/components/links/link';
import LoadingIndicator from 'sentry/components/loadingIndicator';
import {Panel, PanelBody, PanelHeader, PanelItem} from 'sentry/components/panels';
import {IconSubtract} from 'sentry/icons';
import {t} from 'sentry/locale';
import {space} from 'sentry/styles/space';
import {Organization, Project, Team} from 'sentry/types';
import {useTeams} from 'sentry/utils/useTeams';

import {DropdownAddTeam, TeamSelectProps} from './utils';

type Props = TeamSelectProps & {
  canCreateTeam: boolean;
  project: Project;
  /**
   * Used when showing Teams for a Project
   */
  selectedTeams: Team[];
  /**
   * Message to display when the last team is removed
   * if empty no confirm will be displayed.
   */
  confirmLastTeamRemoveMessage?: string;
};

function TeamSelect({
  disabled,
  canCreateTeam,
  confirmLastTeamRemoveMessage,
  project,
  selectedTeams,
  organization,
  onAddTeam,
  onRemoveTeam,
  onCreateTeam,
}: Props) {
  const renderBody = () => {
    const numTeams = selectedTeams.length;
    if (numTeams === 0) {
      return <EmptyMessage>{t('No Teams assigned')}</EmptyMessage>;
    }

    const confirmMessage =
      numTeams === 1 && confirmLastTeamRemoveMessage
        ? confirmLastTeamRemoveMessage
        : null;

    return (
      <React.Fragment>
        {selectedTeams.map(team => (
          <TeamRow
            key={team.slug}
            disabled={disabled}
            confirmMessage={confirmMessage}
            organization={organization}
            team={team}
            onRemoveTeam={slug => onRemoveTeam(slug)}
          />
        ))}
      </React.Fragment>
    );
  };

  const {teams, onSearch, fetching: isLoadingTeams} = useTeams();

  return (
    <Panel>
      <PanelHeader hasButtons>
        {t('Team')}

        <DropdownAddTeam
          disabled={disabled}
          isLoadingTeams={isLoadingTeams}
          isAddingTeamToProject
          canCreateTeam={canCreateTeam}
          onSearch={onSearch}
          onSelect={onAddTeam}
          onCreateTeam={onCreateTeam}
          organization={organization}
          selectedTeams={selectedTeams.map(tm => tm.slug)}
          teams={teams}
          project={project}
        />
      </PanelHeader>

      <PanelBody>{isLoadingTeams ? <LoadingIndicator /> : renderBody()}</PanelBody>
    </Panel>
  );
}

function TeamRow({
  organization,
  team,
  onRemoveTeam,
  disabled,
  confirmMessage,
}: {
  confirmMessage: string | null;
  disabled: boolean;
  onRemoveTeam: Props['onRemoveTeam'];
  organization: Organization;
  team: Team;
}) {
  return (
    <TeamPanelItem data-test-id="team-row-for-project">
      <TeamPanelItemLeft>
        <Link to={`/settings/${organization.slug}/teams/${team.slug}/`}>
          <TeamBadge team={team} />
        </Link>
      </TeamPanelItemLeft>

      <Confirm
        message={confirmMessage}
        bypass={!confirmMessage}
        onConfirm={() => onRemoveTeam(team.slug)}
        disabled={disabled}
      >
        <Button size="xs" icon={<IconSubtract isCircled size="xs" />} disabled={disabled}>
          {t('Remove')}
        </Button>
      </Confirm>
    </TeamPanelItem>
  );
}

const TeamPanelItem = styled(PanelItem)`
  padding: ${space(2)};
  align-items: center;
  justify-content: space-between;
`;

const TeamPanelItemLeft = styled('div')`
  flex-grow: 4;
`;

export default TeamSelect;
