"""Manager for ProgrammeSession."""

from django.db import models


class ProgrammeSessionManager(models.Manager):
    """Manager."""

    # def get_programme_groupby(
    #     self,
    #     athlete: type[Athlete],
    #     level: Literal["year", "month", "week", "day"] = "week",
    #     current: bool = True,
    #     previous: bool = False,
    #     next: bool = False,
    #     *args,
    #     **kwargs
    # ) -> Union[
    #     QuerySet, list[ProgrammeSession]
    # ] | GroupByProgrammeSession | dict[int, GroupByProgrammeSession] | dict[
    #     int, dict[int, GroupByProgrammeSession]
    # ] | dict[
    #     int, dict[int, dict[int, GroupByProgrammeSession]]
    # ]:
    #     """Obtain the programme for a given athlete as a nested groupby.
    #
    #     `level` defaults to "week", but can be changed to define level of nesting \
    #             required for the groupby.
    #     Args:
    #         user (type[Athlete]): Athlete instance model as part of the request.
    #         level (Literal["year", "month", "week", "day"]): nesting for groupby.
    #         current (bool): provide the current `level` set (e.g. current week).
    #         previous (bool): provide the previous `level` week (e.g previous week).
    #         next (bool): provide the programme for the next `level` (e.g. next \
    #                 week).
    #
    #     Returns:
    #         Programme sessions.
    #     """
    #     qs = self.get_queryset()
    #     programmes = (
    #         ProgrammeSession.objects.filter(athlete=athlete)
    #         .order_by("-date")
    #         .annotate(year=ExtractYear(F("date")))
    #         .annotate(month=ExtractMonth(F("date")))
    #         .annotate(week=ExtractWeek(F("date")))
    #         .annotate(day=ExtractDay(F("date")))
    #     )
    #
    #     return programmes
    #
    #     def _generate_nested_defaultdict(depth: int):
    #         return (
    #             defaultdict(lambda: _generate_nested_defaultdict(depth - 1))
    #             if depth
    #             else dict
    #         )
    #
    #     if level == "year":
    #         programmes_group_by = _generate_nested_defaultdict(2)
    #         for p in programmes:
    #             programmes_group_by[p.year][p.pk] = p
    #         return programmes_group_by
    #     elif level == "month":
    #         programmes_group_by = _generate_nested_defaultdict(3)
    #         for p in programmes:
    #             programmes_group_by[p.year][p.month][p.pk] = p
    #         return programmes_group_by
    #     elif level == "week":
    #         programmes_group_by = _generate_nested_defaultdict(4)
    #         for p in programmes:
    #             programmes_group_by[p.year][p.month][p.week][p.pk] = p
    #         return programmes_group_by
    #     elif level == "day":
    #         programmes_group_by = _generate_nested_defaultdict(5)
    #         for p in programmes:
    #             programmes_group_by[p.year][p.month][p.week][p.day][p.pk] = p
    #         return programmes_group_by
    #     else:
    #         return programmes
