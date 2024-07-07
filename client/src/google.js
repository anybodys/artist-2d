import { useEffect, useState } from "react";
import { GoogleOAuthProvider } from '@react-oauth/google';
import './google.css'
import { LoginUri, VotingApi } from './api'

const GOOGLE_OAUTH_CLIENT_ID = process.env.REACT_APP_GOOGLE_OAUTH_CLIENT_ID;

function GoogleButton() {

  const [ userData, setUserData ] = useState([]);

  useEffect(() => {
    VotingApi
      .me()
      .then(userdata => setUserData(userdata))
  }, []);

  const urlParams = new URLSearchParams({
    'next': `${window.location}`
  }).toString();

  return (
    <GoogleOAuthProvider clientId={GOOGLE_OAUTH_CLIENT_ID}>

    <div className="container">
    {userData.email ? (
      <h3 className="card text-left">Welcome, {userData.name}</h3>
    ) : (
      <>
      <div id="g_id_onload"
      data-client_id={GOOGLE_OAUTH_CLIENT_ID}
      data-login_uri={LoginUri + '?' + urlParams}
      data-auto_prompt="false">
      </div>

      <h2>
      <div className="g_id_signin"
      data-type="standard"
      data-size="large"
      data-theme="outline"
      data-text="sign_in_with"
      data-shape="rectangular"
      data-logo_alignment="left">
      </div>
      </h2>
      </>
    )}
    </div>
    </GoogleOAuthProvider>
  );
}

export default GoogleButton;
