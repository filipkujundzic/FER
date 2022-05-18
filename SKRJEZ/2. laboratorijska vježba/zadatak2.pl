#!/usr/bin/perl 

print "Unesite proizvoljan broj brojeva, svaki u novi red. Tocka predstavlja kraj unosa.\n";
@polje = ();
while (<STDIN>){
	chomp($_);
	last if ($_ eq '.');
	push(@polje, $_);
}

$suma = 0;
foreach $i (@polje){
	$suma += $i;
}

print "Zbroj svih clanova polja je: $suma\n";
$broj = $#polje + 1;
print "Broj clanova polja: $broj\n";
$rez = $suma/$broj;
print "Aritmeticka sredina iznosi: $rez";