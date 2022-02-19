from dataengine.service.event import group_events_by_date
from factory.dao_factory import make_event
from factory.util import to_datetime


def test_group_by_date_groups_events_with_the_same_date():
    dt = to_datetime("2022-02-16 08:50:00")
    another_dt = to_datetime("2022-02-17 08:50:00")
    event = make_event(dt, 'some-id', 'body')
    another_event = make_event(another_dt, 'some-id', 'another-body body')
    third_event = make_event(another_dt, 'some-id', 'third-body body')

    grouped = group_events_by_date([event, another_event, third_event])

    assert len(grouped) == 2
    assert grouped['Wed, 16-02-2022'].key == 'Wed, 16-02-2022'
    assert grouped['Wed, 16-02-2022'].value == [event]

    assert grouped['Thu, 17-02-2022'].key == 'Thu, 17-02-2022'
    assert grouped['Thu, 17-02-2022'].value == [another_event, third_event]


def test_group_by_date_groups_events_without_date():
    event = make_event(None, 'some-id', 'body')
    another_event = make_event(None, 'some-id', 'another-body body')

    grouped = group_events_by_date([event, another_event])

    assert len(grouped)
    assert grouped['Not Scheduled'].key == 'Not Scheduled'
    assert grouped['Not Scheduled'].value == [event, another_event]
