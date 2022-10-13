import {Outcome} from 'sentry/types';

export function Outcomes() {
  return {
    start: '2022-07-02T19:00:00Z',
    end: '2022-07-04T18:35:00Z',
    intervals: [
      '2022-07-02T19:00:00Z',
      '2022-07-02T20:00:00Z',
      '2022-07-02T21:00:00Z',
      '2022-07-02T22:00:00Z',
      '2022-07-02T23:00:00Z',
      '2022-07-03T00:00:00Z',
      '2022-07-03T01:00:00Z',
      '2022-07-03T02:00:00Z',
      '2022-07-03T03:00:00Z',
      '2022-07-03T04:00:00Z',
      '2022-07-03T05:00:00Z',
      '2022-07-03T06:00:00Z',
      '2022-07-03T07:00:00Z',
      '2022-07-03T08:00:00Z',
      '2022-07-03T09:00:00Z',
      '2022-07-03T10:00:00Z',
      '2022-07-03T11:00:00Z',
      '2022-07-03T12:00:00Z',
      '2022-07-03T13:00:00Z',
      '2022-07-03T14:00:00Z',
      '2022-07-03T15:00:00Z',
      '2022-07-03T16:00:00Z',
      '2022-07-03T17:00:00Z',
      '2022-07-03T18:00:00Z',
      '2022-07-03T19:00:00Z',
      '2022-07-03T20:00:00Z',
      '2022-07-03T21:00:00Z',
      '2022-07-03T22:00:00Z',
      '2022-07-03T23:00:00Z',
      '2022-07-04T00:00:00Z',
      '2022-07-04T01:00:00Z',
      '2022-07-04T02:00:00Z',
      '2022-07-04T03:00:00Z',
      '2022-07-04T04:00:00Z',
      '2022-07-04T05:00:00Z',
      '2022-07-04T06:00:00Z',
      '2022-07-04T07:00:00Z',
      '2022-07-04T08:00:00Z',
      '2022-07-04T09:00:00Z',
      '2022-07-04T10:00:00Z',
      '2022-07-04T11:00:00Z',
      '2022-07-04T12:00:00Z',
      '2022-07-04T13:00:00Z',
      '2022-07-04T14:00:00Z',
      '2022-07-04T15:00:00Z',
      '2022-07-04T16:00:00Z',
      '2022-07-04T17:00:00Z',
      '2022-07-04T18:00:00Z',
    ],
    groups: [
      {
        by: {outcome: 'client_discard'},
        totals: {'sum(quantity)': 1231344},
        series: {
          'sum(quantity)': [
            0, 1, 1, 1, 94, 1, 1, 0, 566, 179, 1, 1, 1, 0, 222, 6, 287, 465, 83, 7, 0,
            1835, 145, 0, 0, 1, 0, 0, 0, 1, 0, 2, 0, 1, 849, 25331, 147200, 220014,
            189001, 99590, 81288, 134522, 151489, 128585, 41643, 6404, 145, 1381,
          ],
        },
      },
      {
        by: {outcome: 'rate_limited'},
        totals: {'sum(quantity)': 1335469},
        series: {
          'sum(quantity)': [
            0, 0, 0, 0, 191, 0, 0, 0, 385, 0, 0, 0, 0, 0, 345, 0, 445, 276, 56, 0, 0,
            1101, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 656, 45581, 143705, 168077, 168143,
            127756, 114636, 148322, 162904, 153069, 80977, 17299, 512, 1033,
          ],
        },
      },
      {
        by: {outcome: 'accepted'},
        totals: {'sum(quantity)': 19707040},
        series: {
          'sum(quantity)': [
            294117, 281850, 263003, 259581, 246831, 278464, 290677, 242770, 242559,
            248963, 250920, 268994, 296129, 308165, 302398, 301891, 316698, 333888,
            336204, 329735, 323717, 317564, 312407, 307008, 301681, 299652, 276849,
            274486, 298985, 368148, 444434, 423119, 416110, 464443, 526387, 692300,
            720026, 719854, 719658, 719237, 717889, 719757, 718147, 719843, 712099,
            643028, 545065, 311310,
          ],
        },
      },
      {
        by: {outcome: 'filtered'},
        totals: {'sum(quantity)': 13974},
        series: {
          'sum(quantity)': [
            250, 278, 247, 251, 270, 269, 285, 256, 248, 267, 326, 335, 258, 255, 269,
            292, 271, 246, 254, 285, 291, 295, 260, 292, 242, 318, 326, 302, 299, 299,
            321, 310, 320, 371, 323, 331, 286, 256, 275, 316, 294, 295, 301, 282, 391,
            358, 391, 217,
          ],
        },
      },
      {
        by: {outcome: 'invalid'},
        totals: {'sum(quantity)': 38},
        series: {
          'sum(quantity)': [
            0, 1, 2, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 3, 2, 0, 0, 0, 0,
            0, 0, 1, 2, 0, 0, 0, 2, 1, 1, 1, 2, 2, 0, 0, 1, 1, 4, 3, 0, 0, 0,
          ],
        },
      },
    ],
  };
}

export function OutcomesWithReason() {
  return {
    start: '2022-07-02T19:00:00Z',
    end: '2022-07-04T18:35:00Z',
    intervals: [
      '2022-07-02T19:00:00Z',
      '2022-07-02T20:00:00Z',
      '2022-07-02T21:00:00Z',
      '2022-07-02T22:00:00Z',
      '2022-07-02T23:00:00Z',
      '2022-07-03T00:00:00Z',
      '2022-07-03T01:00:00Z',
      '2022-07-03T02:00:00Z',
      '2022-07-03T03:00:00Z',
      '2022-07-03T04:00:00Z',
      '2022-07-03T05:00:00Z',
      '2022-07-03T06:00:00Z',
      '2022-07-03T07:00:00Z',
      '2022-07-03T08:00:00Z',
      '2022-07-03T09:00:00Z',
      '2022-07-03T10:00:00Z',
      '2022-07-03T11:00:00Z',
      '2022-07-03T12:00:00Z',
      '2022-07-03T13:00:00Z',
      '2022-07-03T14:00:00Z',
      '2022-07-03T15:00:00Z',
      '2022-07-03T16:00:00Z',
      '2022-07-03T17:00:00Z',
      '2022-07-03T18:00:00Z',
      '2022-07-03T19:00:00Z',
      '2022-07-03T20:00:00Z',
      '2022-07-03T21:00:00Z',
      '2022-07-03T22:00:00Z',
      '2022-07-03T23:00:00Z',
      '2022-07-04T00:00:00Z',
      '2022-07-04T01:00:00Z',
      '2022-07-04T02:00:00Z',
      '2022-07-04T03:00:00Z',
      '2022-07-04T04:00:00Z',
      '2022-07-04T05:00:00Z',
      '2022-07-04T06:00:00Z',
      '2022-07-04T07:00:00Z',
      '2022-07-04T08:00:00Z',
      '2022-07-04T09:00:00Z',
      '2022-07-04T10:00:00Z',
      '2022-07-04T11:00:00Z',
      '2022-07-04T12:00:00Z',
      '2022-07-04T13:00:00Z',
      '2022-07-04T14:00:00Z',
      '2022-07-04T15:00:00Z',
      '2022-07-04T16:00:00Z',
      '2022-07-04T17:00:00Z',
      '2022-07-04T18:00:00Z',
    ],
    groups: [
      {
        by: {outcome: 'client_discard', reason: 'sample_rate'},
        totals: {'sum(quantity)': 1231333},
        series: {
          'sum(quantity)': [
            0, 1, 1, 1, 94, 1, 1, 0, 566, 179, 1, 1, 1, 0, 222, 6, 287, 465, 83, 7, 0,
            1835, 145, 0, 0, 1, 0, 0, 0, 1, 0, 2, 0, 1, 849, 25331, 147200, 220014,
            189001, 99590, 81288, 134522, 151489, 128585, 41643, 6404, 135, 1380,
          ],
        },
      },
      {
        by: {outcome: 'client_discard', reason: 'network_error'},
        totals: {'sum(quantity)': 11},
        series: {
          'sum(quantity)': [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 1,
          ],
        },
      },
      {
        by: {outcome: 'rate_limited', reason: 'project_abuse_limit'},
        totals: {'sum(quantity)': 1335469},
        series: {
          'sum(quantity)': [
            0, 0, 0, 0, 191, 0, 0, 0, 385, 0, 0, 0, 0, 0, 345, 0, 445, 276, 56, 0, 0,
            1101, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 656, 45581, 143705, 168077, 168143,
            127756, 114636, 148322, 162904, 153069, 80977, 17299, 512, 1033,
          ],
        },
      },
      {
        by: {outcome: 'accepted', reason: 'none'},
        totals: {'sum(quantity)': 19707040},
        series: {
          'sum(quantity)': [
            294117, 281850, 263003, 259581, 246831, 278464, 290677, 242770, 242559,
            248963, 250920, 268994, 296129, 308165, 302398, 301891, 316698, 333888,
            336204, 329735, 323717, 317564, 312407, 307008, 301681, 299652, 276849,
            274486, 298985, 368148, 444434, 423119, 416110, 464443, 526387, 692300,
            720026, 719854, 719658, 719237, 717889, 719757, 718147, 719843, 712099,
            643028, 545065, 311310,
          ],
        },
      },
      {
        by: {outcome: 'filtered', reason: 'Sampled:1'},
        totals: {'sum(quantity)': 13956},
        series: {
          'sum(quantity)': [
            247, 276, 244, 241, 270, 269, 285, 256, 248, 267, 326, 335, 258, 255, 269,
            292, 271, 246, 254, 285, 291, 295, 260, 292, 242, 318, 326, 302, 299, 299,
            321, 310, 320, 371, 323, 331, 286, 256, 275, 316, 294, 295, 301, 282, 391,
            358, 391, 217,
          ],
        },
      },
      {
        by: {outcome: 'filtered', reason: 'Sampled:4'},
        totals: {'sum(quantity)': 3},
        series: {
          'sum(quantity)': [
            1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          ],
        },
      },
      {
        by: {outcome: 'filtered', reason: 'localhost'},
        totals: {'sum(quantity)': 4},
        series: {
          'sum(quantity)': [
            1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          ],
        },
      },
      {
        by: {outcome: 'filtered', reason: 'legacy-browsers'},
        totals: {'sum(quantity)': 11},
        series: {
          'sum(quantity)': [
            1, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          ],
        },
      },
      {
        by: {outcome: 'invalid', reason: 'too_large'},
        totals: {'sum(quantity)': 37},
        series: {
          'sum(quantity)': [
            0, 1, 1, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 3, 2, 0, 0, 0, 0,
            0, 0, 1, 2, 0, 0, 0, 2, 1, 1, 1, 2, 2, 0, 0, 1, 1, 4, 3, 0, 0, 0,
          ],
        },
      },
      {
        by: {outcome: 'invalid', reason: 'invalid_transaction'},
        totals: {'sum(quantity)': 1},
        series: {
          'sum(quantity)': [
            0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          ],
        },
      },
    ],
  };
}

export function OutcomesWithLowProcessedEvents() {
  const otherOutcomesGroups = TestStubs.Outcomes().groups.filter(
    group => group.by.outcome !== 'accepted' && group.by.outcome !== 'client_discard'
  );

  return {
    ...TestStubs.Outcomes(),
    groups: [
      ...otherOutcomesGroups,
      {
        by: {outcome: 'accepted'},
        totals: {'sum(quantity)': 1231342},
        series: {
          'sum(quantity)': [
            0, 0, 0, 1, 94, 1, 1, 0, 566, 179, 1, 1, 1, 0, 222, 6, 287, 465, 83, 7, 0,
            1835, 145, 0, 0, 1, 0, 0, 0, 1, 0, 2, 0, 1, 849, 25331, 147200, 220014,
            189001, 99590, 81288, 134522, 151489, 128585, 41643, 6404, 145, 1381,
          ],
        },
      },
      {
        by: {outcome: 'client_discard'},
        totals: {'sum(quantity)': 18868070},
        series: {
          'sum(quantity)': [
            0, 0, 0, 259581, 246831, 278464, 290677, 242770, 242559, 248963, 250920,
            268994, 296129, 308165, 302398, 301891, 316698, 333888, 336204, 329735,
            323717, 317564, 312407, 307008, 301681, 299652, 276849, 274486, 298985,
            368148, 444434, 423119, 416110, 464443, 526387, 692300, 720026, 719854,
            719658, 719237, 717889, 719757, 718147, 719843, 712099, 643028, 545065,
            311310,
          ],
        },
      },
    ],
  };
}

export function OutcomesWithoutClientDiscarded() {
  return {
    ...TestStubs.OutcomesWithReason(),
    groups: TestStubs.OutcomesWithReason().groups.filter(
      group => group.by.outcome !== Outcome.CLIENT_DISCARD
    ),
  };
}
