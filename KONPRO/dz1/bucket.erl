-module(bucket).
-export([bucket_sort/2]).
-import(lists, [max/1, nth/2, split/2]).

%Function for initialization of buckets
init_array(1) -> [[],[]];
init_array(N) -> [[]|init_array(N - 1)].

%Function for finding the index of the bucket in which to insert element
find_bucket_index(G, N, Max) when (G * N) div Max == 0 -> 1;
find_bucket_index(G, N, Max) -> (G * N) div Max.  

%Function for appending a element to the right bucket 
add_to_bucket([], List, I, Count)    when I == Count ->
    [List];
add_to_bucket([H|T], List, I, Count) when I =/= Count ->
    [H|add_to_bucket(T, List, I, Count + 1)];
add_to_bucket([_|T], List, I, Count) when I == Count  ->
    [List|T].

%Function for scattering elements into buckets 
scatter(Buckets, [], _, _)    -> Buckets;
scatter(Buckets, [G|R], N, Max) ->
    I = find_bucket_index(G, N, Max),
    Del = nth(I, Buckets),
    New_buckets = add_to_bucket(Buckets, [G]++Del, I, 1),
    scatter(New_buckets, R, N, Max).

%Function for spliting a list and merging it back together using merge
merge_sort([L]) -> [L]; 
merge_sort(List)   ->
    {L1,L2} = split(length(List) div 2, List),
    merge(merge_sort(L1), merge_sort(L2)).

%Comparison of list elements
merge(L1, L2)         -> merge(L1, L2, []).
merge([], L2, Sorted) -> Sorted++L2;
merge(L1, [], Sorted) -> Sorted++L1;
merge([H1|T1], [H2|T2], Sorted) when H2>=H1 -> merge(T1, [H2|T2], Sorted++[H1]);
merge([H1|T1], [H2|T2], Sorted) when H1>H2  -> merge([H1|T1], T2, Sorted++[H2]).

%Function for appending together merge sorted buckets
merge_sort_buckets([], Sorted) -> Sorted;
merge_sort_buckets([H|T], Sorted) when H == [] ->
    merge_sort_buckets(T,Sorted);
merge_sort_buckets([H|T], Sorted)              -> 
    Sorted_bucket = merge_sort(H),
    merge_sort_buckets(T, Sorted++Sorted_bucket).

%Main function, takes a list and number of buckets
bucket_sort(List, 1) ->
    merge_sort_buckets([List], []);
bucket_sort(List, N) when (N =< 0) or (List == []) ->
    [];
bucket_sort(List, N) -> 
    Buckets = init_array(N - 1),
    Filled_buckets = scatter(Buckets, List, N, max(List)),
    merge_sort_buckets(Filled_buckets, []).

