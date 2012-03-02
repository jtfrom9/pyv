module add(
    input [3:0] a,
    input [3:0] b,
    output [3:0] c);

   reg [3:0]     c;

   always@* begin
      c <= a + b;
   end
   
endmodule


module main;
   reg [3:0] a, b;
   wire [3:0] c;
   
   add add0(.a(a), .b(b), .c(c));

   task set(input [3:0] in1, input [3:0] in2);
      begin
         a = in1;
         b = in2;
         #1 $display("a=%d, b=%d, c=%d",a,b,c);
      end
   endtask

   integer i,j;
   
   initial begin
      for(i=0; i<10; i=i+1)
        for(j=0; j<10; j=j+1)
          #10 set(i,j);
      $finish;
   end
endmodule
