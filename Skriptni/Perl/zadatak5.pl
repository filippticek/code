#!/usr/bin/perl

open CONFIG, $ARGV[$#ARGV];
chomp($redak = <CONFIG>);
@udio = split /;/, $redak;
@rez_uk = ();

while (defined($redak = <CONFIG>)) {
	chomp($redak);
	($jmbag, $prezime, $ime, @bod) = split /;/, $redak;
	$rezultat = 0;
	foreach (0..$#bod) {
		if ($bod[$_] ne "-") {
			$rezultat += ($bod[$_] * $udio[$_]);
		}
	}
	push @rez_uk, $rezultat . ";" . "$prezime, $ime ($jmbag) :";
}

@sortirano = sort {$b <=> $a} @rez_uk;

print "Lista po rangu:\n";
print "---------------------------\n";
foreach (0..$#sortirano) {
	@podaci = split /;/, $sortirano[$_];
	printf "%3d. %s : %0.2f\n", $_ +1, $podaci[1], $podaci[0]; 
}


