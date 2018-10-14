import React, { Component } from 'react';

import { Gestures } from '../api/gestures.js';
import { Button } from 'react-bootstrap';

export default class Gesture extends Component {

    deleteThisGesture() {
        Gestures.remove(this.props.gesture._id);
    }

    render() {
        return (
            <tr>
                <td>{this.props.gesture.text}</td>
                <td>{this.props.gesture.command}</td>
                <td><Button className="delete" bsStyle="danger" onClick={this.deleteThisGesture.bind(this)}>Remove</Button>
                </td>
            </tr>
        );
    }
}
