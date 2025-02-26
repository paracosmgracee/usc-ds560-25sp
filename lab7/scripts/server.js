
const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');

const app = express();
app.use(cors());

const db = mysql.createConnection({
    host: "dsci560mysqlserver.mysql.database.azure.com",
    user: "superlogin",
    password: "GroupForResume@123",
    database: "oil_wells"
});

db.connect(err => {
    if (err) {
        console.error("Database connection failed:", err);
    } else {
        console.log("Connected to MySQL Database.");
    }
});

// API to get well data
app.get('/wells', (req, res) => {
    db.query("SELECT * FROM oil_wells_information", (err, results) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.json(results);
        }
    });
});

app.listen(3000, () => console.log('Server running on http://localhost:3000'));
