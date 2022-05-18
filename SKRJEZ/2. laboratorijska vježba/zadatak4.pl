#!/usr/bin/perl

while ($line = <>) {

	@s = split(" ",$line);

	@pocetak = split(":",$s[1]);
	@predaja = split(":",$s[4]);

	@v = split(";",$s[0]);
	@v1 = split("-",$v[3]);

	@w = split(";",$s[3]);
	@w1 = split("-",$w[1]);

	if( $pocetak[0] != $predaja[0] or $v1[2] != $w1[2]) {
		@a = split(';',$line);
		@p = split(" ",$a[3]);
		print "$a[0] $a[1] $a[2] - PROBLEM: $p[0] $p[1] --> $a[4]";
	}
}