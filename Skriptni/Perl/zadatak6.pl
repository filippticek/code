#!/usr/bin/perl
use open ':locale';
use locale;

$broj = $ARGV[$#ARGV];
%prefiks;
@prefiks_polje;
@words_all = ();

while (defined($redak = <>)){
	@words = split / /, $redak;
	#print "@words\n";
	foreach (@words){
		#print "$_\n";
		if (/^([a-zA-Z]{$broj})/) {
			$pre = $1; 
		}
		else {
			$pre = "";
		}
		#print "$pre\n";
		$pre =~ tr/A-Z/a-z/; 
		$postoji = 0;
		#print "@words_all\n";
		push @words_all, $pre;
		foreach $pref (@prefiks_polje) {
			if ( $pre eq $pref) {
				$postoji = 1;
			}

		}
		if ($postoji == 0) {
			$prefiks{$pre} = 1;
			push @prefiks_polje, $pre;
		}
		else {
			$count = 0;
			foreach $w (@words_all) {
				if ($pre eq $w){
					$count += 1;
				}
			}
			$prefiks{$pre} = $count;
		}
	}

}
@sortirano = sort @prefiks_polje;
shift @sortirano;
foreach (@sortirano) {
	print "$_ : $prefiks{$_}\n";
}
