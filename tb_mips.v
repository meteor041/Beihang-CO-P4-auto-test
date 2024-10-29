`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   02:05:14 10/29/2024
// Design Name:   mips
// Module Name:   E:/Documents/computer_organization/work/mips/tb_mips.v
// Project Name:  mips
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: mips
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

// `include "mips.v"
module tb_mips;

	// Inputs
	reg clk;
	reg reset;

	// Instantiate the Unit Under Test (UUT)
	mips uut (
		.clk(clk), 
		.reset(reset)
	);
	//initial begin
//    $dumpfile("wave.vcd");
//    $dumpvars(0, mips);
	//end
	initial begin

		// Initialize Inputs
		reset = 1;
		clk = 0;
		// Wait 100 ns for global reset to finish
		#100;
        
		// Add stimulus here
		reset = 0;
		#2000 $stop(0);
	end
	always #50 clk = ~clk;
      
endmodule

