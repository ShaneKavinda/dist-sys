use PITR;
GO



-- create the table to store Payroll data
CREATE TABLE PayrollRecords (
	Payroll_ID INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
	TFN INT NOT NULL,
	Net_Wage DECIMAL(19,4) NOT NULL,
	Tax_Withheld DECIMAL(19,4) NOT NULL,
	Pay_Period_Start DATE,
	Pay_Period_End DATE,
	);
GO

-- create the table to store Payroll data
CREATE TABLE TaxData (
	TFN INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
	Taxable_Income DECIMAL(19,4) NOT NULL,
	Total_Tax_Withheld DECIMAL(19,4) NOT NULL,
	Total_Net_Income DECIMAL(19,4) NOT NULL,
	Medicare_Levy DECIMAL(19,4),
	Medicare_Levy_Surcharge DECIMAL(19,4),
	Tax_Refund DECIMAL(19,4)
	);
GO