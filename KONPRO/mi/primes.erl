-module(primes).
-export([get_primes/1]).

%Iterates between numbers in a given list
%And calls a function to fill the gap with prime numbers
get_primes(List) ->
    get_primes(List, []).
get_primes([H], List) when is_integer(H) ->
    List++[H];
get_primes([H|T], List) ->
    [Last|_] = T,
    Filled = fill_primes(H, Last),
    get_primes(T, List++[H]++Filled).

%Returns a list with prime numbers that are in between X and Last
fill_primes(X, Last) when X < Last ->
    fill_primes(X+1, Last, []);
fill_primes(_, _) -> [].

fill_primes(X, Last, List) when X < Last ->
    Condition = is_prime(X),
    Result = test_condition(Condition, X),
    fill_primes(X + 1, Last, List++Result);
fill_primes(_, _, List) ->
    List.
    
%If a number is prime return a list, otherwise return a empty list
test_condition(true, X) -> [X];
test_condition(false, _) -> [].

%Function for calculating if a number is prime
is_prime(X) when X =< 3 -> X > 1;
is_prime(X) when X rem 2 == 0 -> false;
is_prime(X) when X rem 3 == 0 -> false;
is_prime(X) -> is_prime(X, 5).
is_prime(X, I) when X rem I == 0 ->
    false;
is_prime(X, I) ->
    Pow = math:pow(I, 2),
    if Pow < X -> is_prime(X, I + 2);
       true -> true
    end.
