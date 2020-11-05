#!/usr/bin/perl

open CONFIG, $ARGV[$#ARGV];

@datum = ();
@time = ();

while (defined($redak = <CONFIG>)) {
	chomp($redak);
	($grupa, $opis, $broj_studenata, $datum_dan, $vrijeme, $trajanje, $prostorija) = split /\t/, $redak;
	push @datum, $datum_dan;
	push @time, ($vrijeme . " " . $prostorija . " " . $broj_studenata);
}

foreach $i (0..$#datum) {
	foreach $j ($i..$#datum) {
		if ($datum[$i] eq $datum[$j]) {
			if ($time[$i] gt $time[$j]){
				$temp = $datum[$i];
				$datum[$i] = $datum[$j];
				$datum[$j] = $temp;
				$temp = $time[$i];
				$time[$i] = $time[$j];
				$time[$j] = $temp;
			}
			
		}
		if ($datum[$i] gt $datum[$j]) {
			$temp = $datum[$i];
			$datum[$i] = $datum[$j];
			$datum[$j] = $temp;
			$temp = $time[$i];
			$time[$i] = $time[$j];
			$time[$j] = $temp;
		}
	}
}

foreach $i (0..$#datum) {
	printf "%2d. %s %s\n", $i+1, $datum[$i], $time[$i];
}
