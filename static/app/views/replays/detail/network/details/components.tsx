import {Fragment, ReactNode, useState} from 'react';
import styled from '@emotion/styled';

import {KeyValueTable, KeyValueTableRow} from 'sentry/components/keyValueTable';
import {Tooltip} from 'sentry/components/tooltip';
import {IconChevron} from 'sentry/icons';
import {t} from 'sentry/locale';
import {space} from 'sentry/styles/space';

export const Indent = styled('div')`
  padding-left: ${space(4)};
`;

const NotFoundText = styled('span')`
  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeSmall};
`;

const WarningText = styled('span')`
  color: ${p => p.theme.errorText};
`;

export function Warning({warnings}: {warnings: undefined | string[]}) {
  if (warnings?.includes('JSON_TRUNCATED') || warnings?.includes('TEXT_TRUNCATED')) {
    return (
      <WarningText>{t('Truncated (~~) due to exceeding 150k characters')}</WarningText>
    );
  }

  if (warnings?.includes('INVALID_JSON')) {
    return <WarningText>{t('Invalid JSON')}</WarningText>;
  }

  return null;
}

export function SizeTooltip({children}: {children: ReactNode}) {
  return (
    <Tooltip
      title={t('It is possible the network transfer size is smaller due to compression.')}
    >
      {children}
    </Tooltip>
  );
}

export function keyValueTableOrNotFound(
  data: undefined | Record<string, string>,
  notFoundText: string
) {
  return data ? (
    <StyledKeyValueTable noMargin>
      {Object.entries(data).map(([key, value]) => (
        <KeyValueTableRow key={key} keyName={key} value={<span>{value}</span>} />
      ))}
    </StyledKeyValueTable>
  ) : (
    <Indent>
      <NotFoundText>{notFoundText}</NotFoundText>
    </Indent>
  );
}

const SectionTitle = styled('dt')``;

const SectionTitleExtra = styled('span')`
  flex-grow: 1;
  text-align: right;
  font-weight: normal;
`;

const SectionData = styled('dd')`
  font-size: ${p => p.theme.fontSizeExtraSmall};
`;

const ToggleButton = styled('button')`
  background: ${p => p.theme.background};
  border: 0;
  color: ${p => p.theme.headingColor};
  font-size: ${p => p.theme.fontSizeSmall};
  font-weight: 600;
  line-height: ${p => p.theme.text.lineHeightBody};

  width: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: ${space(1)};

  padding: ${space(0.5)} ${space(1)};

  :hover {
    background: ${p => p.theme.backgroundSecondary};
  }
`;

export function SectionItem({
  children,
  title,
  titleExtra,
}: {
  children: ReactNode;
  title: ReactNode;
  titleExtra?: ReactNode;
}) {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <Fragment>
      <SectionTitle>
        <ToggleButton aria-label={t('toggle section')} onClick={() => setIsOpen(!isOpen)}>
          <IconChevron direction={isOpen ? 'down' : 'right'} size="xs" />
          {title}
          {titleExtra ? <SectionTitleExtra>{titleExtra}</SectionTitleExtra> : null}
        </ToggleButton>
      </SectionTitle>
      <SectionData>{isOpen ? children : null}</SectionData>
    </Fragment>
  );
}

const StyledKeyValueTable = styled(KeyValueTable)`
  & > dt {
    font-size: ${p => p.theme.fontSizeSmall};
    padding-left: ${space(4)};
  }
  & > dd {
    ${p => p.theme.overflowEllipsis};
    font-size: ${p => p.theme.fontSizeSmall};
    display: flex;
    justify-content: flex-end;
    white-space: normal;
    text-align: right;
  }
`;
