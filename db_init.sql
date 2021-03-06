DROP DATABASE IF EXISTS wholesale;
CREATE DATABASE IF NOT EXISTS wholesale;
USE wholesale;

DROP TABLE IF EXISTS warehouse;
DROP TABLE IF EXISTS district;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS "order";
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS orderline;
DROP TABLE IF EXISTS stock;

CREATE TABLE IF NOT EXISTS warehouse
(
    W_ID       INT,
    W_NAME     VARCHAR(10),
    W_STREET_1 VARCHAR(20),
    W_STREET_2 VARCHAR(20),
    W_CITY     VARCHAR(20),
    W_STATE    CHAR(2),
    W_ZIP      CHAR(9),
    W_TAX      DECIMAL(4, 4),
    W_YTD      DECIMAL(12, 2),
    PRIMARY KEY (W_ID),
	FAMILY     warehouse_1 (W_ID, W_YTD),
    FAMILY     warehouse_2 (W_NAME, W_STREET_1, W_STREET_2, W_CITY, W_STATE, W_ZIP, W_TAX)
);

IMPORT INTO warehouse (W_ID, W_NAME, W_STREET_1, W_STREET_2, W_CITY, W_STATE, W_ZIP, W_TAX, W_YTD)
     CSV DATA (
       'nodelocal://1/warehouse.csv'
     );
    

CREATE TABLE IF NOT EXISTS district
(
	D_W_ID      INT REFERENCES warehouse (W_ID),
	D_ID        INT,
	D_NAME      VARCHAR(10),
	D_STREET_1  VARCHAR(20),
	D_STREET_2  VARCHAR(20),
	D_CITY      VARCHAR(20),
	D_STATE     CHAR(2),
	D_ZIP       CHAR(9),
	D_TAX       DECIMAL(4,4),
	D_YTD       DECIMAL(12,2),
	D_NEXT_O_ID INT,
	PRIMARY KEY (D_W_ID, D_ID),
	FAMILY      district_1 (D_ID, D_W_ID, D_YTD, D_NEXT_O_ID),
    FAMILY      district_2 (D_NAME, D_STREET_1, D_STREET_2, D_CITY, D_STATE, D_ZIP, D_TAX)
);

IMPORT INTO district (D_W_ID, D_ID, D_NAME, D_STREET_1, D_STREET_2, D_CITY, D_STATE, D_ZIP, D_TAX, D_YTD, D_NEXT_O_ID)
     CSV DATA (
       'nodelocal://1/district.csv'
     );
    

CREATE TABLE IF NOT EXISTS customer 
(
	C_W_ID         INT,
	C_D_ID         INT,
	C_ID           INT,
	C_FIRST        VARCHAR(16),
	C_MIDDLE       CHAR(2),
	C_LAST         VARCHAR(16),
	C_STREET_1     VARCHAR(20),
	C_STREET_2     VARCHAR(20),
	C_CITY         VARCHAR(20),
	C_STATE        CHAR(2),
	C_ZIP          CHAR(9),
	C_PHONE        CHAR(16),
	C_SINCE        TIMESTAMP,
	C_CREDIT       CHAR(2),
	C_CREDIT_LIM   DECIMAL(12,2),
	C_DISCOUNT     DECIMAL(4,4),
	C_BALANCE      DECIMAL(12,2),
	C_YTD_PAYMENT  FLOAT,
	C_PAYMENT_CNT  INT,
	C_DELIVERY_CNT INT,
	C_DATA         VARCHAR(500),
	PRIMARY KEY (C_W_ID, C_D_ID, C_ID),
	FOREIGN KEY (C_W_ID, C_D_ID) references district (D_W_ID, D_ID),
	FAMILY         customer_1 (C_ID, C_W_ID, C_D_ID, C_BALANCE, C_YTD_PAYMENT, C_PAYMENT_CNT, C_DELIVERY_CNT),
    FAMILY         customer_2 (C_FIRST, C_MIDDLE, C_LAST, C_STREET_1, C_STREET_2, C_CITY, C_STATE, C_ZIP, C_PHONE, C_SINCE, C_CREDIT, C_CREDIT_LIM, C_DISCOUNT, C_DATA)
);

IMPORT INTO customer 
(
	C_W_ID,
	C_D_ID,
	C_ID,
	C_FIRST,
	C_MIDDLE,
	C_LAST,
	C_STREET_1,
	C_STREET_2,
	C_CITY,
	C_STATE,
	C_ZIP,
	C_PHONE,
	C_SINCE,
	C_CREDIT,
	C_CREDIT_LIM,
	C_DISCOUNT,
	C_BALANCE,
	C_YTD_PAYMENT,
	C_PAYMENT_CNT,
	C_DELIVERY_CNT,
	C_DATA
	) CSV DATA ('nodelocal://1/customer.csv');


CREATE TABLE IF NOT EXISTS "order"
(
	O_W_ID       INT,
	O_D_ID       INT,
	O_ID         INT,
	O_C_ID       INT,
	O_CARRIER_ID INT,
	O_OL_CNT     DECIMAL(2,0),
	O_ALL_LOCAL  DECIMAL(1,0),
	O_ENTRY_D    TIMESTAMP,
	PRIMARY KEY (O_W_ID, O_D_ID, O_ID),
	FOREIGN KEY (O_W_ID, O_D_ID, O_C_ID) REFERENCES customer (C_W_ID, C_D_ID, C_ID),
	FAMILY       order_1 (O_ID, O_W_ID, O_D_ID, O_C_ID, O_CARRIER_ID),
    FAMILY       order_2 (O_OL_CNT, O_ALL_LOCAL, O_ENTRY_D)
);

IMPORT INTO "order"
(
	O_W_ID,
	O_D_ID,
	O_ID,
	O_C_ID,
	O_CARRIER_ID,
	O_OL_CNT,
	O_ALL_LOCAL,
	O_ENTRY_D
	) CSV DATA ('nodelocal://1/order.csv') WITH nullif = 'null';


CREATE TABLE IF NOT EXISTS item 
(
	I_ID    INT,
	I_NAME  VARCHAR(24),
	I_PRICE DECIMAL(5,2),
	I_IM_ID INT,
	I_DATA  VARCHAR(50),
	PRIMARY KEY (I_ID),
	FAMILY  item_1 (I_ID, I_PRICE),
	FAMILY  item_2 (I_NAME, I_IM_ID, I_DATA)
);

IMPORT INTO item 
(
	I_ID,
	I_NAME,
	I_PRICE,
	I_IM_ID,
	I_DATA
	) CSV DATA ('nodelocal://1/item.csv');


CREATE TABLE IF NOT EXISTS orderline 
(
	OL_W_ID        INT,
	OL_D_ID        INT,
	OL_O_ID        INT,
	OL_NUMBER      INT,
	OL_I_ID        INT,
	OL_DELIVERY_D  TIMESTAMP,
	OL_AMOUNT      DECIMAL(7,2),
	OL_SUPPLY_W_ID INT,
	OL_QUANTITY    DECIMAL(2,0),
	OL_DIST_INFO   CHAR(24),
	PRIMARY KEY (OL_W_ID, OL_D_ID, OL_O_ID, OL_NUMBER),
	FOREIGN KEY (OL_W_ID, OL_D_ID, OL_O_ID) REFERENCES "order" (O_W_ID, O_D_ID, O_ID),
	FAMILY         order_line_1 (OL_NUMBER, OL_O_ID, OL_W_ID, OL_D_ID, OL_DELIVERY_D),
    FAMILY         order_line_2 (OL_I_ID, OL_AMOUNT, OL_SUPPLY_W_ID, OL_QUANTITY, OL_DIST_INFO)
);

IMPORT INTO orderline 
(
	OL_W_ID,
	OL_D_ID,
	OL_O_ID,
	OL_NUMBER,
	OL_I_ID,
	OL_DELIVERY_D,
	OL_AMOUNT,
	OL_SUPPLY_W_ID,
	OL_QUANTITY,
	OL_DIST_INFO
	) CSV DATA ('nodelocal://1/order-line.csv') WITH nullif = 'null';



CREATE TABLE IF NOT EXISTS stock (
	S_W_ID       INT          REFERENCES warehouse (W_ID),
	S_I_ID       INT          REFERENCES item (I_ID),
	S_QUANTITY   DECIMAL(4,0),
	S_YTD        DECIMAL(8,2),
	S_ORDER_CNT  INT,
	S_REMOTE_CNT INT,
	S_DIST_01    CHAR(24),
	S_DIST_02    CHAR(24),
	S_DIST_03    CHAR(24),
	S_DIST_04    CHAR(24),
	S_DIST_05    CHAR(24),
	S_DIST_06    CHAR(24),
	S_DIST_07    CHAR(24),
	S_DIST_08    CHAR(24),
	S_DIST_09    CHAR(24),
	S_DIST_10    CHAR(24),
	S_DATA       VARCHAR(50),
	PRIMARY KEY (S_W_ID, S_I_ID),
	FAMILY       stock_1 (S_W_ID, S_I_ID, S_QUANTITY, S_YTD, S_ORDER_CNT, S_REMOTE_CNT),
    FAMILY       stock_2 (S_DIST_01, S_DIST_02, S_DIST_03, S_DIST_04, S_DIST_05, S_DIST_06, S_DIST_07, S_DIST_08, S_DIST_09, S_DIST_10, S_DATA)
);

IMPORT INTO stock 
(
	S_W_ID,
	S_I_ID,
	S_QUANTITY,
	S_YTD,
	S_ORDER_CNT,
	S_REMOTE_CNT,
	S_DIST_01,
	S_DIST_02,
	S_DIST_03,
	S_DIST_04,
	S_DIST_05,
	S_DIST_06,
	S_DIST_07,
	S_DIST_08,
	S_DIST_09,
	S_DIST_10,
	S_DATA
	) CSV DATA ('nodelocal://1/stock.csv');

