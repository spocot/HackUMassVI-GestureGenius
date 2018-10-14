import React, { Component } from 'react';
import ReactDOM from 'react-dom';

import { withTracker } from 'meteor/react-meteor-data';

import { Gestures } from '../api/gestures.js';
import Gesture from './Gesture.js';

import { Table, PageHeader, Panel, Form, FormControl, Button } from 'react-bootstrap';

const bigboisty = {
    width: '45%'
}

const smallboisty = {
    width: '10%'
}

class App extends Component {
    handleSubmit(event) {
        event.preventDefault();

        const gestureT = ReactDOM.findDOMNode(this.refs.gestureInput).value.trim();
        const commandT = ReactDOM.findDOMNode(this.refs.commandInput).value.trim();

        Gestures.insert({
            text: gestureT,
            command: commandT,
            createdAt: new Date(),
        });

        ReactDOM.findDOMNode(this.refs.gestureInput).value = '';
        ReactDOM.findDOMNode(this.refs.commandInput).value = '';
    }

    renderGestures() {
        return this.props.gestures.map((gesture) => (
            <Gesture key={gesture._id} gesture={gesture} />
        ));
    }

    render() {
        return (
            <div className="container">
                <PageHeader>Gestures</PageHeader>
                <Panel>
                    <Panel.Body>
                        <form onSubmit={this.handleSubmit.bind(this)} className="new-gesture form-inline">
                            <FormControl style={bigboisty} type="text" ref="gestureInput" placeholder="New Gesture Pattern"/>
                            <FormControl style={bigboisty} type="text" ref="commandInput" placeholder="New Smart Command"/>
                            <Button style={smallboisty} type="submit">Add</Button>
                        </form>
                    </Panel.Body>
                </Panel>
                
                <Table striped bordered condensed hover>
                    <thead>
                        <tr>
                            <th className="col-xs-4">Gesture Mapping</th>
                            <th className="col-xs-7">Command</th>
                            <th className="col-xs-1"></th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.renderGestures()}
                    </tbody>
                </Table>
            </div>
        );
    }
}

export default withTracker(() => {
    return {
        gestures: Gestures.find({}, { sort: { createdAt: -1} }).fetch(),
    };
})(App);
