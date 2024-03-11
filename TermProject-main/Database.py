import sqlite3

class Database:
    
    def __init__(self):
        self.con = sqlite3.connect("DATABASE.db")
        self.cur = self.con.cursor()
        self.currentmove = 0
        self.lastmove = 0

        #instantiate the database with the needed tables
        self.cur.executescript("""
        PRAGMA foreign_keys = 0; --Disable ALL foreign key constraint checks

        --GAMEROUND(RID, P1Name, P1Number, P2Name, P2Number)
        CREATE TABLE IF NOT EXISTS GAMEROUND
            (RID INTEGER PRIMARY KEY AUTOINCREMENT, 
            P1Name VARCHAR(50),
            P1Number INTEGER,
            P2Name VARCHAR(50),
            P2Number INTEGER
            );
            
        --GAMEMOVE(MID, PlayerNum, Position, RID)
        CREATE TABLE IF NOT EXISTS GAMEMOVE
            (MID INTEGER,
            PlayerNum INTEGER,
            Position INTEGER,
            RID INTEGER,
            PRIMARY KEY (MID, RID)
            FOREIGN KEY (RID) REFERENCES GAMEROUND(RID)
            );
            
        """)

    def dropTables(self):
        #this drops the GAMEROUND and GAMEMOVE tables
        self.cur.executescript("""DROP TABLE IF EXISTS GAMEROUND;
            DROP TABLE IF EXISTS GAMEMOVE;""")

    def storeRound(self, P1Name, P1Number, P2Name, P2Number):
        #this creates a round to store moves in
        self.cur.execute("""
        INSERT INTO GAMEROUND(P1Name, P1Number, P2Name, P2Number)
        VALUES(?, ?, ?, ?);

        """, (P1Name, P1Number, P2Name, P2Number) )
        self.con.commit()
        
        #return the created RID
        self.cur.execute("SELECT MAX(RID) FROM GAMEROUND")
        self.lastmove = 0
        return self.cur.fetchone()

    def storeMove(self, PlayerNum, Position, RID):
        #this stores the data from this particular move
        self.lastmove += 1 #leave the lastmove here becuase it needs to occur before the self.cur.execute

        self.cur.execute("""
        INSERT INTO GAMEMOVE(MID, PlayerNum, Position, RID)
        VALUES (?, ?, ?, ?);

        """, (self.lastmove, PlayerNum, Position, RID) )
        self.con.commit()
        

    def printMoves(self):
        #this prints out all of the events in the given round
        self.currentmove += 1
        self.cur.execute("SELECT MAX(RID) FROM GAMEROUND")
        rid = self.cur.fetchone()
        print("RID",rid)
        self.cur.execute("SELECT * FROM GAMEMOVE WHERE RID=?", rid)
        print("current: ", self.currentmove, " last: ", self.lastmove)
        if self.currentmove <= self.lastmove:
            for row in self.cur.fetchall():
                if row[0] == self.currentmove:
                    print("REVIEW", row)
                    return row
        else:
            return (0, 0, 0, 0)
    
    def setNextMove(self, num):
        self.currentmove = num
