--------------------------------------------------------------------------------
-- Procesador MIPS con pipeline curso Arquitectura 2020-2021
--
-- Daniel Mohedano	<daniel.mohedano@estudiante.uam.es>
-- Silvia Sopeña	<silvia.sopenna@estudiante.uam.es>
--------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity processor is
  port(
    Clk         : in  std_logic; -- Reloj activo en flanco subida
    Reset       : in  std_logic; -- Reset asincrono activo nivel alto
    -- Instruction memory
    IAddr      : out std_logic_vector(31 downto 0); -- Direccion Instr
    IDataIn    : in  std_logic_vector(31 downto 0); -- Instruccion leida
    -- Data memory
    DAddr      : out std_logic_vector(31 downto 0); -- Direccion
    DRdEn      : out std_logic;                     -- Habilitacion lectura
    DWrEn      : out std_logic;                     -- Habilitacion escritura
    DDataOut   : out std_logic_vector(31 downto 0); -- Dato escrito
    DDataIn    : in  std_logic_vector(31 downto 0)  -- Dato leido
  );
end processor;

architecture rtl of processor is

  component alu
    port(
      OpA : in std_logic_vector (31 downto 0);
      OpB : in std_logic_vector (31 downto 0);
      Control : in std_logic_vector (3 downto 0);
      Result : out std_logic_vector (31 downto 0);
      Zflag : out std_logic
    );
  end component;

  component reg_bank
     port (
        Clk   : in std_logic; -- Reloj activo en flanco de subida
        Reset : in std_logic; -- Reset as�ncrono a nivel alto
        A1    : in std_logic_vector(4 downto 0);   -- Direcci�n para el puerto Rd1
        Rd1   : out std_logic_vector(31 downto 0); -- Dato del puerto Rd1
        A2    : in std_logic_vector(4 downto 0);   -- Direcci�n para el puerto Rd2
        Rd2   : out std_logic_vector(31 downto 0); -- Dato del puerto Rd2
        A3    : in std_logic_vector(4 downto 0);   -- Direcci�n para el puerto Wd3
        Wd3   : in std_logic_vector(31 downto 0);  -- Dato de entrada Wd3
        We3   : in std_logic -- Habilitaci�n de la escritura de Wd3
     );
  end component reg_bank;

  component control_unit
     port (
        -- Entrada = codigo de operacion en la instruccion:
        Instr   : in  std_logic_vector (31 downto 0);
        -- Seniales para el PC
        Branch   : out  std_logic; -- 1 = Ejecutandose instruccion branch
		    Jump     : out  std_logic; -- 1 = Ejecutandose instruccion jump 
        -- Seniales relativas a la memoria
        MemToReg : out  std_logic; -- 1 = Escribir en registro la salida de la mem.
        MemWrite : out  std_logic; -- Escribir la memoria
        MemRead  : out  std_logic; -- Leer la memoria
        -- Seniales para la ALU
        ALUSrc   : out  std_logic;                     -- 0 = oper.B es registro, 1 = es valor inm.
        ALUOp    : out  std_logic_vector (2 downto 0); -- Tipo operacion para control de la ALU
        -- Seniales para el GPR
        RegWrite : out  std_logic; -- 1=Escribir registro
        RegDst   : out  std_logic  -- 0=Reg. destino es rt, 1=rd
     );
  end component;

  component alu_control is
    port (
      -- Entradas:
      ALUOp  : in std_logic_vector (2 downto 0); -- Codigo de control desde la unidad de control
      Funct  : in std_logic_vector (5 downto 0); -- Campo "funct" de la instruccion
      -- Salida de control para la ALU:
      ALUControl : out std_logic_vector (3 downto 0) -- Define operacion a ejecutar por la ALU
    );
  end component alu_control;
 
  -- IF Stage 
	signal PC_next        : std_logic_vector(31 downto 0); -- Next PC 
	signal PC_reg         : std_logic_vector(31 downto 0); -- Signal for the PC register
	signal PC_plus4_IF    : std_logic_vector(31 downto 0); -- PC+4
	signal Instr_IF	      : std_logic_vector(31 downto 0); -- Instruction code
	signal PCWrite		  : std_logic; 					   -- Enable for PC Register
  
  -- ID Stage
	signal Instr_ID	      : std_logic_vector(31 downto 0);        -- Instruction code
	signal PC_plus4_ID    : std_logic_vector(31 downto 0);        -- PC+4
	signal Inm_ext_ID     : std_logic_vector(31 downto 0);        -- Sign extended lower half of instruction
	signal reg_RS_ID, reg_RT_ID : std_logic_vector(31 downto 0);  -- Data read from RS and RT
	signal load_use_hazard: std_logic;	-- Control signal activated by load use data hazards

	signal Ctrl_Jump_ID, Ctrl_Branch_ID, Ctrl_MemWrite_ID, Ctrl_MemRead_ID,  Ctrl_ALUSrc_ID, Ctrl_RegDest_ID, Ctrl_MemToReg_ID, Ctrl_RegWrite_ID : std_logic;
	signal Ctrl_ALUOP_ID  : std_logic_vector(2 downto 0); -- Control signals needed in ID stage

  -- EX Stage
	signal reg_RS_EX, reg_RT_EX : std_logic_vector(31 downto 0); -- Data read from RS and RT
	signal Instr_EX	      : std_logic_vector(31 downto 0);  -- Instruction code
	signal PC_plus4_EX    : std_logic_vector(31 downto 0);  -- PC+4
	signal AluControl     : std_logic_vector(3 downto 0);   -- ALU control signal (ALUControl->ALU)
	signal Alu_Op1        : std_logic_vector(31 downto 0);  -- First operand of ALU
	signal Alu_Op2        : std_logic_vector(31 downto 0);  -- Second operand of ALU
	signal res_ForwardB	: std_logic_vector(31 downto 0);  -- Result of the forwarding B
	signal ALU_Res_EX: std_logic_vector(31 downto 0);       -- ALU Result
	signal ALU_Igual_EX   : std_logic;                      -- Z flag of the ALU
	signal reg_RD_EX      : std_logic_vector(4 downto 0);   -- Address of register RD
	signal Addr_Branch_EX : std_logic_vector(31 downto 0);  -- Address of the branch
	signal Addr_Jump_EX   : std_logic_vector(31 downto 0);  -- Address of the jump
	signal Inm_ext_EX	    : std_logic_vector(31 downto 0);  -- Sign extended lower half of instruction

	signal Ctrl_Jump_EX, Ctrl_Branch_EX, Ctrl_MemWrite_EX, Ctrl_MemRead_EX,  Ctrl_ALUSrc_EX, Ctrl_RegDest_EX, Ctrl_MemToReg_EX, Ctrl_RegWrite_EX : std_logic;
	signal Ctrl_ALUOP_EX  : std_logic_vector(2 downto 0); -- Control signals needed in EX stage
  
  
  -- MEM Stage
	signal ALU_Igual_MEM  : std_logic; -- Z flag of the ALU
	signal reg_RD_MEM     : std_logic_vector(4 downto 0); -- Address of register RD
	signal ALU_Res_MEM    : std_logic_vector(31 downto 0);-- ALU Result
	signal reg_RT_MEM		  : std_logic_vector(31 downto 0);-- Data read from RT
	signal dataIn_Mem_MEM : std_logic_vector(31 downto 0);-- Data read from memory
	signal Addr_Jump_MEM  : std_logic_vector(31 downto 0);-- Address of the jump
	signal Addr_Branch_MEM: std_logic_vector(31 downto 0);-- Address of the branch
	signal Addr_Jump_dest : std_logic_vector(31 downto 0);-- Final address in case of a jump (jump or branch)
	signal PC_Src  		    : std_logic; -- Control signal for PC source

	signal Ctrl_Jump_MEM, Ctrl_Branch_MEM, Ctrl_MemWrite_MEM, Ctrl_MemRead_MEM, Ctrl_MemToReg_MEM, Ctrl_RegWrite_MEM : std_logic; -- Control signals needed in MEM stage
  
  -- WB Stage
	signal dataIn_Mem_WB  : std_logic_vector(31 downto 0);  -- Data read from memory
	signal reg_RD_data    : std_logic_vector(31 downto 0);  -- Write data for register RD
	signal reg_RD_WB      : std_logic_vector(4 downto 0);   -- Address of register RD
	signal ALU_Res_WB     : std_logic_vector(31 downto 0);  -- ALU result
	signal Ctrl_RegWrite_WB, Ctrl_MemToReg_WB : std_logic;  -- Control signals needed in WB stage
  
  -- Enables for stage registers
	signal enable_IF_ID	  : std_logic;
	signal enable_ID_EX	  : std_logic;
	signal enable_EX_MEM	: std_logic;
	signal enable_MEM_WB	: std_logic;
  
  --Data Forwarding Unit Signals
	signal ForwardA : std_logic_vector(1 downto 0); -- Control signal for mux of input A
	signal ForwardB : std_logic_vector(1 downto 0); -- Control signal for mux of input B  

begin
  -- PORT MAPPING
  RegsMIPS : reg_bank
  port map (
    Clk   => Clk,
    Reset => Reset,
    A1    => Instr_ID(25 downto 21),
    Rd1   => reg_RS_ID,
    A2    => Instr_ID(20 downto 16),
    Rd2   => reg_RT_ID,
    A3    => reg_RD_WB,
    Wd3   => reg_RD_data,
    We3   => Ctrl_RegWrite_WB
  );

  UnidadControl : control_unit
  port map(
    Instr   => Instr_ID,
    -- Señales para el PC
    --Jump   => CONTROL_JUMP,
    Branch   => Ctrl_Branch_ID,
	  Jump     => Ctrl_Jump_ID,
    -- Señales para la memoria
    MemToReg => Ctrl_MemToReg_ID,
    MemWrite => Ctrl_MemWrite_ID,
    MemRead  => Ctrl_MemRead_ID,
    -- Señales para la ALU
    ALUSrc   => Ctrl_ALUSrc_ID,
    ALUOP    => Ctrl_ALUOP_ID,
    -- Señales para el GPR
    RegWrite => Ctrl_RegWrite_ID,
    RegDst   => Ctrl_RegDest_ID
  );

  Alu_control_i: alu_control
  port map(
    -- Entradas:
    ALUOp  => Ctrl_ALUOP_EX, -- Codigo de control desde la unidad de control
    Funct  => Instr_EX(5 downto 0), -- Campo "funct" de la instruccion
    -- Salida de control para la ALU:
    ALUControl => AluControl -- Define operacion a ejecutar por la ALU
  );

  Alu_MIPS : alu
  port map (
    OpA     => Alu_Op1,
    OpB     => Alu_Op2,
    Control => AluControl,
    Result  => ALU_Res_EX,
    Zflag   => ALU_Igual_EX
  );


  ---- IF STAGE ----
  PC_reg_proc: process(Clk, Reset)
  begin
    if Reset = '1' then
      PC_reg <= (others => '0');
    elsif rising_edge(Clk) and PCWrite='1' then
      PC_reg <= PC_next;
    end if;
  end process;

  PC_plus4_IF <= PC_reg + 4;
  IAddr <= PC_reg;
  Instr_IF <= IDataIn;
  
  PCWrite <= '0' when load_use_hazard='1' else '1';

  Reg_IFID: process (Clk, Reset)
  begin
	  if Reset = '1' then
		  PC_plus4_ID <= (others=>'0');
		  Instr_ID 	<= (others=>'0');
	  elsif rising_edge(Clk) and enable_IF_ID='1' then
		  PC_plus4_ID <= PC_plus4_IF;
		  Instr_ID 	<= Instr_IF;
	  end if;
  end process;

  ---- ID STAGE ----
  Inm_ext_ID     <= x"FFFF" & Instr_ID(15 downto 0) when Instr_ID(15)='1' else
                    x"0000" & Instr_ID(15 downto 0);
					
	load_use_hazard <= '1' when Ctrl_MemRead_EX = '1' and ( Instr_EX(20 downto 16) = Instr_ID(25 downto 21) or Instr_EX(20 downto 16) = Instr_ID(20 downto 16)) else '0';

  Reg_IDEX: process (Clk, Reset)
  begin
    if Reset = '1' then
		Instr_EX		<= (others=>'0');
		reg_RS_EX 		<= (others=>'0');
		reg_RT_EX 		<= (others=>'0');
		Inm_ext_EX		<= (others=>'0');
		PC_plus4_EX		<= (others=>'0');
		Ctrl_Jump_EX	<= '0';
		Ctrl_Branch_EX	<= '0';
		Ctrl_MemWrite_EX<= '0';
		Ctrl_MemRead_EX	<= '0';
		Ctrl_ALUSrc_EX	<= '0';
		Ctrl_RegDest_EX	<= '0';
		Ctrl_MemToReg_EX<= '0';
		Ctrl_RegWrite_EX<= '0';
		Ctrl_ALUOP_EX	<= (others=>'0');
	elsif load_use_hazard='1' and rising_edge(Clk) then
		Ctrl_Jump_EX	<= '0';
		Ctrl_Branch_EX	<= '0';
		Ctrl_MemWrite_EX<= '0';
		Ctrl_MemRead_EX	<= '0';
		Ctrl_ALUSrc_EX	<= '0';
		Ctrl_RegDest_EX	<= '0';
		Ctrl_MemToReg_EX<= '0';
		Ctrl_RegWrite_EX<= '0';
		Ctrl_ALUOP_EX	<= (others=>'0');
    elsif rising_edge(Clk) and enable_ID_EX='1' then
		Instr_EX 		<= Instr_ID;
		reg_RS_EX		<= reg_RS_ID;
		reg_RT_EX		<= reg_RT_ID;
		Inm_ext_EX		<= Inm_ext_ID;
		PC_plus4_EX		<= PC_plus4_ID;
		Ctrl_Jump_EX	<= Ctrl_Jump_ID;
		Ctrl_Branch_EX	<= Ctrl_Branch_ID;
		Ctrl_MemWrite_EX<= Ctrl_MemWrite_ID;
		Ctrl_MemRead_EX	<= Ctrl_MemRead_ID;
		Ctrl_ALUSrc_EX	<= Ctrl_ALUSrc_ID;
		Ctrl_RegDest_EX	<= Ctrl_RegDest_ID;
		Ctrl_MemToReg_EX<= Ctrl_MemToReg_ID;
		Ctrl_RegWrite_EX<= Ctrl_RegWrite_ID;
		Ctrl_ALUOP_EX	<= Ctrl_ALUOP_ID;
    end if;
  end process;

  ---- EX STAGE ----
  Addr_Jump_EX      <= PC_plus4_EX(31 downto 28) & Instr_EX(25 downto 0) & "00";
  Addr_Branch_EX    <= PC_plus4_EX + ( Inm_ext_EX(29 downto 0) & "00");

  Alu_Op1 <= 	ALU_Res_MEM	when ForwardA = "10" else
				reg_RD_data when ForwardA = "01" else
				reg_RS_EX;
  res_ForwardB <= 	ALU_Res_MEM	when ForwardB = "10" else
					reg_RD_data when ForwardB = "01" else
					reg_RT_EX;
  Alu_Op2    <= res_ForwardB when Ctrl_ALUSrc_EX = '0' else Inm_ext_EX;
  reg_RD_EX     <= Instr_EX(20 downto 16) when Ctrl_RegDest_EX = '0' else Instr_EX(15 downto 11);
  
  
  ForwardA <= "10" when Ctrl_RegWrite_MEM = '1' and reg_RD_MEM /= "00000" and reg_RD_MEM = Instr_EX(25 downto 21) else
			  "01" when Ctrl_RegWrite_WB = '1' and reg_RD_WB /= "00000" and reg_RD_WB = Instr_EX(25 downto 21) else
			  "00";
  
  ForwardB <= "10" when Ctrl_RegWrite_MEM = '1' and reg_RD_MEM /= "00000" and reg_RD_MEM = Instr_EX(20 downto 16) else
			  "01" when Ctrl_RegWrite_WB = '1' and reg_RD_WB /= "00000" and reg_RD_WB = Instr_EX(20 downto 16) else
			  "00";

  Reg_EXMEM: process (Clk, Reset)
  begin
    if Reset = '1' then
      reg_RD_MEM 			<= (others=>'0');
      reg_RT_MEM 			<= (others=>'0');
      ALU_Res_MEM			<= (others=>'0');
      Addr_Jump_MEM		<= (others=>'0');
      Addr_Branch_MEM		<= (others=>'0');
      Ctrl_Jump_MEM		<= '0';
      Ctrl_Branch_MEM		<= '0';
      ALU_Igual_MEM		<= '0';
      Ctrl_MemWrite_MEM	<= '0';
      Ctrl_MemRead_MEM	<= '0';
      Ctrl_MemToReg_MEM	<= '0';
      Ctrl_RegWrite_MEM	<= '0';
    elsif rising_edge(Clk) and enable_EX_MEM='1' then
      reg_RD_MEM 			<= reg_RD_EX;
      reg_RD_MEM 			<= reg_RD_EX;
      reg_RT_MEM 			<= res_ForwardB;
      ALU_Res_MEM			<= ALU_Res_EX;
      Addr_Jump_MEM		<= Addr_Jump_EX;
      Addr_Branch_MEM		<= Addr_Branch_EX;
      Ctrl_Jump_MEM		<= Ctrl_Jump_EX;
      Ctrl_Branch_MEM		<= Ctrl_Branch_EX;
      ALU_Igual_MEM		<= ALU_Igual_EX;
      Ctrl_MemWrite_MEM	<= Ctrl_MemWrite_EX;
      Ctrl_MemRead_MEM	<= Ctrl_MemRead_EX;
      Ctrl_MemToReg_MEM	<= Ctrl_MemToReg_EX;
      Ctrl_RegWrite_MEM	<= Ctrl_RegWrite_EX;
    end if;
  end process;

  ---- MEM STAGE ----
  Addr_Jump_dest <= Addr_Jump_MEM   when Ctrl_Jump_MEM='1' else
                    Addr_Branch_MEM when Ctrl_Branch_MEM='1' else
                    (others =>'0');
  PC_Src  <= Ctrl_Jump_MEM or (Ctrl_Branch_MEM and ALU_Igual_MEM);
  PC_next <= Addr_Jump_dest when PC_Src = '1' else PC_plus4_IF;

  DAddr      <= ALU_Res_MEM;
  DDataOut   <= reg_RT_MEM;
  DWrEn      <= Ctrl_MemWrite_MEM;
  dRdEn      <= Ctrl_MemRead_MEM;
  dataIn_Mem_MEM <= DDataIn;
  
  Reg_MEMWB: process (Clk, Reset)
  begin
    if Reset = '1' then
      reg_RD_WB		<= (others=>'0');
      ALU_Res_WB		<= (others=>'0');
      dataIn_Mem_WB	<= (others=>'0');
      Ctrl_MemToReg_WB<= '0';
      Ctrl_RegWrite_WB<= '0';
    elsif rising_edge(Clk) and enable_MEM_WB='1' then
      reg_RD_WB		<= reg_RD_MEM;
      ALU_Res_WB		<= ALU_Res_MEM;
      dataIn_Mem_WB	<= dataIn_Mem_MEM;
      Ctrl_MemToReg_WB<= Ctrl_MemToReg_MEM;
      Ctrl_RegWrite_WB<= Ctrl_RegWrite_MEM;
    end if;
  end process;

  ---- WB STAGE ----
  reg_RD_data <= dataIn_Mem_WB when Ctrl_MemToReg_WB = '1' else ALU_Res_WB;

  
  -- Stage register enables
  enable_IF_ID	<= '0' when load_use_hazard='1' else '1';
  enable_ID_EX	<= '1';
  enable_EX_MEM	<= '1';
  enable_MEM_WB	<= '1';
 
end architecture;
