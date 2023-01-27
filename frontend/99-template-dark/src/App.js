import {BrowserRouter, Routes, Route} from "react-router-dom";
import {Link, useNavigate, useLocation} from "react-router-dom";
import queryString from 'query-string'

import "./App.css";
import {useEffect} from "react";
//
//?
const GoogleOAuth = () => {
    return <div className='google-btn'>
        <a href="https://accounts.google.com/o/oauth2/auth?client_id=loremipsum&redirect_uri=http://localhost:8000/login&scope=email&response_type=code"
           className="oauth-button">
            Sign in with Google
        </a>
    </div>
}

const ParseQuery = () => {
    const location = useLocation()
    const query = queryString.parse(location.search)
    console.log(query)
    const url = `http://127.0.0.1:8000/login?auth_code=${query["code"]}`
    useEffect(() => {
        fetch(url)
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(e => console.log(e))
    });
    return <>
        <div>{query["code"]}</div>
        <div>
            <a href="http://localhost:3000">main</a>
        </div>
    </>
}


function App() {
    return (
        <BrowserRouter>
            <div className="App">
                <Routes>
                    <Route path="/" element={<GoogleOAuth/>}>
                    </Route>
                    <Route path="/query" element={<ParseQuery/>}/>

                </Routes>
                <a href="http://localhost:3000/query">query</a>

            </div>
        </BrowserRouter>
    );
}

export default App;
