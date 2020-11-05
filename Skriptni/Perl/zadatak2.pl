#!/usr/bin/perl

chomp(@niz=<STDIN>);
$sum = 0;

foreach $broj (@niz) {
	$sum +=$broj;
}

print $sum/($#niz+1);
