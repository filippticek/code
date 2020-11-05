#!/usr/bin/perl
$prvi = 0;
while (defined($redak = <>)) {
	if ($prvi == 0) {
		$prvi = 1;
	}
	else {
		($jmbag, $prezime, $ime, $termin, $zakljucano) = split /;/, $redak;
		@term = split / /, $termin;
		@lock = split / /, $zakljucano;
		$prvi_sat = 0;
		
		if ($term[0] ne $lock[0]) {
			$prvi_sat = 1;
		}
		
		($sat, $minuta) = split /:/, $term[1];
		$term_t = $sat*3600 + $minuta*60;
		($sat, $minuta, $sec) = split /:/, $lock[1];
		$lock_t = $sat*3600 + $minuta*60 + $sec;
		
		if (($lock_t - $term_t) > 3600) {
			$prvi_sat = 1;
		}

		if ($prvi_sat) {
			print "$jmbag $prezime $ime - PROBLEM: $term[0] $term[1] --> $zakljucano";
		}
	}
}
