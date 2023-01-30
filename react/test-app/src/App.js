import './App.css';
import React, { useEffect, useState } from 'react'
import {Amplify, Auth} from 'aws-amplify'

Amplify.configure(
  {
    region: process.env.REACT_APP_AWS_REGION,
    userPoolId: process.env.REACT_APP_COGNITO_USER_POOL_ID,
    userPoolWebClientId: process.env.REACT_APP_COGNITO_WEBCLIENT_ID
  }
);

function App() {
  // user is initially undefined, it is defined when a challenge is sent, it is xxx when authenticated...
  const [email, setEmail] = useState("");
  const [challenge, setChallenge] = useState("");
  const [tryNumber, setTryNumber] = useState(0);
  const [disableButton, setDisableButton] = useState(false);
  const [cognitoUser, setCognitoUser] = useState();
  const [userExists, setUserExists] = useState(false);
  const [authenticated, setAuthenticated] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    Auth.currentSession()
      .then((user)=>{
        setAuthenticated(true);
        setMessage(user.idToken.payload.email+" authenticated.");
        setTryNumber(0);
      })
      .catch(()=>{
        setMessage("");
        if (tryNumber > 0) setMessage(`Incorrect code. Please retry.`);
        setAuthenticated(false);
      });
  }, [email, tryNumber])

  return (
    <div className="App">
      <p>{message}</p>
      {authenticated?"":
        <p>Email address:
          {userExists?email:
            <input type="text"
                   value={email}
                   onChange={(e) => setEmail(e.target.value)}/>
          }
        </p>
      }
      {userExists && !authenticated?
        <p>Code:
          <input type="text"
                 value={challenge}
                 onChange={(e) => setChallenge(e.target.value)}/>
        </p>:
        ""
      }
      {!authenticated?
        <button onClick={() => userExists? submitChallenge(): requestChallenge()}
                disabled={disableButton}>
          Submit
        </button>:
        <button onClick={() => {
          setDisableButton(true);
          Auth.signOut().then(()=>{setUserExists(false);setEmail("");setChallenge("");
            setMessage("");setTryNumber(0);setCognitoUser(undefined);
            setDisableButton(false);})
        }}
                disabled={disableButton}>
          Signout
        </button>
      }
    </div>
  );

  function requestChallenge() {
    setDisableButton(true);
    const params = {
      username: email,
      password: getRandomString(30),
    }
    Auth.signUp(params) // Signup the user (so that signin is possible)
      .then(()=> {
        Auth.signIn(email) // Initiate the authentication to start the custom authentication flow
          .then((user)=>{setCognitoUser(user); setUserExists(true);})
          .catch((error)=>console.log(`Error signing in: ${error}`))
          .finally(() => setDisableButton(false))
      })
      .catch((error)=>{
        if (error.code.startsWith("UsernameExistsException")) {
          Auth.signIn(email)
            .then((user)=>{setCognitoUser(user); setUserExists(true);})
            .catch((error)=>console.log(`Error signing in: ${error}`))
            .finally(()=> setDisableButton(false))
        } else {
          console.log(`Error signing up: ${error}`);
          setDisableButton(false);
        }
      });

    function getRandomString(bytes) {
      const randomValues = new Uint8Array(bytes);
      window.crypto.getRandomValues(randomValues);
      return Array.from(randomValues).map(intToHex).join('Az@'); //Az@ to fill possible password format constraint
    }
    function intToHex(nr) {
      return nr.toString().padStart(2, '0');
    }
  }

  function submitChallenge() {
    setDisableButton(true);
    Auth.sendCustomChallengeAnswer(cognitoUser, challenge)
      .then((user)=> {
        setCognitoUser(user);
      })
      .catch((error)=>console.log(`Error sending Custom Challenge Answer: ${error}`))
      .finally(()=>{setDisableButton(false);setTryNumber(tryNumber+1)});
  }
}
export default App;