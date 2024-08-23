const express = require('express');
const cors = require('cors');
const bcrypt = require('bcrypt');
const sqlite3 = require('sqlite3');
const bodyParser = require('body-parser');
const {join} = require("node:path");

const app = express();
const port = 3000;

app.use(cors());
app.use(bodyParser.json());

// req (request) - this is the data the function needs
// res (response) - what the server responds (Eg code 200).
// Code 200 means true. Thus, the program will open the next url
app.post('/login', (req, res) => {
    const { username, password } = req.body;

    console.log(`Received login attempt for username: ${username}`);

    // getting the absolute path of the ERP system database
    const dbPath = join(__dirname, '../erp_system.db');

    let conn = new sqlite3.Database(dbPath, (err) => {
        if (err) {
            console.error('Error opening database:', err.message);
            return res.status(500).json({ error: 'Database connection error' });
        }
    });

    conn.get("SELECT username, password_hash FROM users WHERE username =?", [username], async (err, user) => {
        if (err) {
            console.error('Error fetching data:', err.message);
            return res.status(500).json({ error: 'Error fetching user data' });
        }

        if (user) {
            try {
                const match = await bcrypt.compare(password, user.password_hash);
                if (match) {
                    console.log(`${username} Has been loggedIn successfully!`);
                    return res.status(200).json({ success: true, message: 'Login successful' });
                } else {
                    return res.status(401).json({ success: false, message: 'Incorrect password' });
                }
            } catch (error) {
                console.error('Error comparing passwords:', error);
                return res.status(500).json({ error: 'Error during password comparison' });
            }
        } else {
            return res.status(404).json({ success: false, message: 'User not found' });
        }
    });

    conn.close((err) => {
        if (err) {
            console.error("Error closing database:", err.message);
        }
    });
});

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});

// Summary:

// Why we use JSON Parsing for data communication between the server and client:

// Frontend HTML Form Submission:

// The form in accountManagement.html submits login data (username and password)
// to your backend server using a POST request with JSON payload.
// Backend Handling in Node.js:

//Your Node.js server receives the POST request,
// parses the JSON payload to extract the login details,
// and performs authentication by querying the SQLite database.

// In your case, JSON parsing is used to handle the data being sent and received between the client and server.
// Ensuring proper JSON handling on both the client and server sides will help in accurately processing and responding to requests,
// preventing errors related to data format and enabling smooth communication between your application components.