/*
 * # Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * # SPDX-License-Identifier: MIT-0
 */

import '@aws-amplify/ui-react/styles.css';
import {Route, Routes} from 'react-router-dom';
import {withAuthenticator} from '@aws-amplify/ui-react';
import Home from "./routes/home";
import Dashboard from './routes/dashboard';
// import { applyMode, applyDensity, Density, Mode } from '@cloudscape-design/global-styles';


function App({signOut, user}) {
    // applyMode(Mode.Dark);

    return (
        <Routes>
            <Route index element={<Home />}/>
            <Route path="/dashboard/:key/*" element={<Dashboard userid={user.username}/>}/>
        </Routes>
    );
}

export default withAuthenticator(App);