const express = require('express');
const cors = require('cors');
const bcrypt = require('bcrypt');
const sqlite3 = require('sqlite3').verbose();
const bodyParser = require('body-parser');
const {join} = require("node:path");
const path = require('path');


const app = express();
const port = 3000;

app.use(express.static(path.join(__dirname, 'public')));
app.use(cors());
app.use(bodyParser.json());

// req (request) - this is the data the function needs
// res (response) - what the server responds (Eg code 200).
// Code 200 means true. Thus, the program will open the next url
app.post('/login', (req, res) => {
    const { inputUsername, inputPassword } = req.body;

    console.log(`Received login attempt for username: ${inputUsername}`);

    // getting the absolute path of the ERP system database (process.env.DATABASE_URL) makes it dynamic
    const dbPath = process.env.DATABASE_URL || join(__dirname, '../database/erp_system.db');


    // Creating a connection to the database
    let conn = new sqlite3.Database(dbPath, (err) => {
        // If there is an error connecting, return the error message
        if (err) {
            console.error('Error opening database:', err.message);
            // res = response - 500 = the server encountered an unexpected condition that prevented it fulfilling the request.
            return res.status(500).json({ error: 'Database connection error' });
        }
    });

    // Retrieving the username and password_hash from the users table where the username matches the provided value (the parameter "username"
    conn.get("SELECT username, password_hash FROM users WHERE username =?", [inputUsername], async (err, user) => {
        // If there is an error - return the error message
        if (err) {
            console.error('Error fetching data:', err.message);
            // res = response - code 500 = the server encountered an unexpected condition that prevented it fulfilling the request.
            return res.status(500).json({ error: 'Error fetching user data' });
        }

        // if user === true
        if (user) {
            try {
                // Hashing the input password ("password") and then comparing if they're a match.
                const match = await bcrypt.compare(inputPassword, user.password_hash);
                // If they are a match, Output the message
                if (match) {
                    console.log(`${inputUsername} Has been loggedIn successfully!`);
                    return res.status(200).json({ success: true, message: 'Login successful' });
                // Of they are not a match, Output the error message
                } else {
                    return res.status(401).json({ success: false, message: 'Incorrect password' });
                }
            // res = response - code 500 = the server encountered an unexpected condition that prevented it fulfilling the request.
            } catch (error) {
                console.error('Error comparing passwords:', error);
                return res.status(500).json({ error: 'Error during password comparison' });
            }
        // If user is not found in the database
        } else {
            return res.status(404).json({ success: false, message: 'User not found' });
        }
    });

    // End the connection
    conn.close((err) => {
        // If there is an error - return the error message
        if (err) {
            console.error("Error closing database:", err.message);
        }
    });
});

app.post('/create', async (req, res) => {
    const { inputUsername, inputPassword } = req.body;

    console.log(`Received account creation attempt for username: ${inputUsername}`)

    const dbPath = join(__dirname, '../database/erp_system.db');

    let conn = new sqlite3.Database(dbPath, (err) => {
        if (err) {
            console.error('Error opening database:', err.message);
            return res.status(500).json({error: 'Error creating database'});
        }
    });

    try {
        // Hashing the password
        const password_hash = await bcrypt.hash(inputPassword, 10);
        // declaring the variable
        const reorder_level = 0;

        // Inserting the data into the SQLite database - This creates a new account
        conn.run('INSERT INTO users (username, password_hash, reorder_level) VALUES (?, ?, ?)', [inputUsername, password_hash, reorder_level], (err, result) => {
            // If there is an error, return the error message
            if (err) {
                console.error('Error adding user data:', err.message);
                return res.status(500).json({error: 'Username already taken'});
            }
            // If there is an error, return the error message
            console.log(`${inputUsername} Has been created successfully!`);
            return res.status(200).json({ success: true, message: 'Account created successfully' });
        });
    // If there is an error, return the error message
    } catch (error) {
        console.error('Error hashing password:', error.message);
        return res.status(500).json({error: 'Error creating database'});
    }

    // Close the connection with the database
    conn.close((err) => {
        // If there is an error, return the error message
        if (err) {
            console.error('Error creating database:', err.message);
        }
    });
});

// Starts the server application and have it listen for incoming network requests on a specific port (3000).
// It also logs a message to the console indicating that the server is running and provides the url where it can be accessed.
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