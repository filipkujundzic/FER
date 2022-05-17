library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.std_logic_arith.all;


entity enkoder is
    port (
	btn_left, btn_right, btn_up, btn_down, btn_center: in std_logic;
	code: out std_logic_vector(6 downto 0)
    );
end enkoder;


architecture behavioral of enkoder is
    signal btns: std_logic_vector(4 downto 0);

begin

    btns <= btn_down & btn_left & btn_center & btn_up & btn_right;

    with btns select
    code <=
	"0000000" when "00000", -- no tone
	"0000000" when "10000", -- no tone
	"0111100" when "01000", -- c -> MIDI #60
	"0111110" when "00100", -- d -> MIDI #62
	"1000000" when "00010", -- e -> MIDI #64
	"1000001" when "00001", -- f -> MIDI #65
	"1000011" when "11000", -- g -> MIDI #67
	"1000101" when "10100", -- a -> MIDI #69
	"1000111" when "10010", -- h -> MIDI #71
	"1001000" when "10001", -- c -> MIDI #72
	"-------" when others ; -- don't care

end;
