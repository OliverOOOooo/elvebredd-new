CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    robloxUsername TEXT,
    profilePicture TEXT,
    blocked TEXT,
    friends TEXT,
    friendRequestsSent TEXT,
    friendRequestsReceived TEXT,
    inventory TEXT,
    wishlist TEXT,
    notifications TEXT,
    trades TEXT,
    inbox TEXT,
    pending TEXT,
    completedTrades TEXT
);

CREATE TABLE Trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner INTEGER,
    acceptedBy INTEGER,
    acceptedByUsername TEXT,
    acceptedByRobloxUsername TEXT,
    public INTEGER,
    visibleTo TEXT,
    completed INTEGER
);