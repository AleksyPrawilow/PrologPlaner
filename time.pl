time_to_minutes(H, M, Total) :- Total is H * 60 + M.
minutes_to_time(Min, time(H, M)) :- H is Min // 60, M is Min mod 60.

schedule_classes(Start, End, ClassDuration, Recess, Classes) :- schedule_classes_helper(Start, End, ClassDuration, Recess, [], ClassesReversed), reverse(ClassesReversed, Classes).

schedule_classes_helper(Current, End, ClassDuration, Recess, Acc, Classes) :-
    NextEnd is Current + ClassDuration,
    ( NextEnd =< End -> minutes_to_time(Current, StartTime), minutes_to_time(NextEnd, EndTime), NextStart is NextEnd + Recess, schedule_classes_helper(NextStart, End, ClassDuration, Recess, [StartTime-EndTime|Acc], Classes); Classes = Acc).