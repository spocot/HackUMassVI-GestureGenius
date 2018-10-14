import { Meteor } from 'meteor/meteor';
import React from 'react';
import ReactDOM from 'react-dom';

import App from '../imports/ui/App.js';

import './main.html'

Meteor.startup(() => {
    console.log("Starting app...");
    e = document.getElementById('render-target');
    console.log(e);
    ReactDOM.render(<App />, e);
});
