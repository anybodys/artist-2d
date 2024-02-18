import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <Museum/>
    </div>
  );
}


class Museum extends React.Component {
    render() {
        // TODO(kmd): This should come from the API. :)
        const paintingsData = [{
            publicLink: 'https://storage.googleapis.com/artist-2d.appspot.com/gen-0/0427b526-d632-41a1-b995-1b07a24befba.jpg',
            generation: 0,
            artistId: 'example-artist-id-1'
        },{
            publicLink: 'https://storage.googleapis.com/artist-2d.appspot.com/gen-0/0427b526-d632-41a1-b995-1b07a24befba.jpg',
            generation: 0,
            artistId: 'example-artist-id-2'
        }];

        const paintings = paintingsData.map(pd =>
            this.renderPainting(pd)
        );

        return (<div>{paintings}</div>);
    }


    renderPainting(pd) {
        return (
                <Painting
            key={pd.artistId}
            props={pd}
                />
        );
    }
}


class Painting extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            publicUrl: props.props.publicLink,
            artistId: props.props.artistId
        };
    }

    render() {
        return (
                <img
            className="Painting"
            src={this.state.publicUrl}
            alt={"Computer generated abstract art by " + this.state.artistId}
                />
        );
    }
}

export default App;
