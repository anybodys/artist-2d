import React, { useCallback, useEffect, useState } from "react";
import './App.css';
import { VotingApi } from './api'
import GoogleButton from './google';

export const UserContext = React.createContext([]);


function App() {
  const [user, setUserData] = useState(UserContext);
  const [paintingsData, setData] = useState([]);

  useEffect(() => {
    VotingApi
      .getArt()
      .then(data => setData(data['art']))
  }, []);

  return (
    <div className="App">
      <UserContext.Provider value={user}>
        <GoogleButton
          userData={user}
          setUserCallback={useCallback((newUserData) => { setUserData(newUserData) }, [])}
        />
        <div className="container">
          <h2 className="card">Rendered Art</h2>
        </div>

        <div className="container">{paintingsData ? paintingsData.map(
          pd => <Painting key={pd.artist_id} props={pd} />) : 'Loading...'}
        </div>
      </UserContext.Provider>
    </div>
  );
}


class Painting extends React.Component {
  static contextType = UserContext;

  constructor(props) {
    super(props);
    this.state = {
      publicUrl: props.props.public_link,
      artistId: props.props.artist_id,
      heart: false,
    };
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    if (!this.context.email) {
      alert("Please log in to vote for this painting.");
      return;
    }
    VotingApi.vote(this.state.artistId);
    this.setState(prevState => ({
      heart: !prevState.heart
    }));
  }

  render() {
    return (
      <div className="Painting" style={{ position: "relative", display: "inline-block" }}>
        <img
          className="card"
          src={this.state.publicUrl}
          alt={"Computer generated abstract art by " + this.state.artistId}
          onClick={this.handleClick}
        />
        <span
          style={{
            position: "absolute",
            top: 8,
            right: 8,
            fontSize: "2rem",
            color: this.state.heart ? "red" : "black",
            textShadow: "0 0 2px white"
          }}
        >
          {this.state.heart ? "♥" : "♡"}
        </span>
      </div>
    );
  }
}

export default App;
