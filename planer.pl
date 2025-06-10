:- dynamic teacher/1.
:- dynamic course/2.
:- dynamic slot/1.
:- dynamic room/1.

room(a).
room(b).

schedule(Schedule) :-
    findall(course(Name, Teacher), course(Name, Teacher), Courses),
    assign(Courses, [], Schedule),
    valid(Schedule).

assign([], Acc, Acc).
assign([course(Name, Teacher)|Rest], Acc, Schedule) :- slot(Slot), room(Room), assign(Rest, [entry(Name, Teacher, Slot, Room) | Acc], Schedule), valid([entry(Name, Teacher, Slot, Room) | Acc]).

valid(Schedule) :- no_teacher_conflicts(Schedule), no_room_conflicts(Schedule).

no_teacher_conflicts([]).
no_teacher_conflicts([entry(Name, Teacher, Slot, _)|Rest]) :- \+ (member(entry(Name2, Teacher, Slot, _), Rest), Name \= Name2), no_teacher_conflicts(Rest).

no_room_conflicts([]).
no_room_conflicts([entry(Name, _, Slot, Room)|Rest]) :- \+ (member(entry(Name2, _, Slot, Room), Rest), Name \= Name2), no_room_conflicts(Rest).

all_schedules(All) :- findall(Schedule, schedule(Schedule), All).

get_entry_data(entry(Przedmiot, Prowadzacy, Godzina, Sala), Przedmiot, Prowadzacy, Godzina, Sala).