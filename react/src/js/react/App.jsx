/**
 * Entry-point for the react code in the app.
 * Allows us to map various URLs to page-components
 */

import React from "react";
import { Route, Switch } from "react-router-dom";

import PageNotFound from "./help/PageNotFound";
import Header from "./misc/Header";
import LoginView from "./auth/LoginView";
import RegisterView from "./auth/RegisterView";

import AuthActions from "./auth/AuthActions";
import ProfileView from "./profile/ProfileView";

export default class App extends React.Component {
    componentDidMount() {
        AuthActions.parseLoginCookies();
    }

    render() {
        return (
            <div className="core-app-view">
                <Header />
                <Switch>
                    <Route path="/login" component={LoginView} />
                    <Route path="/register" component={RegisterView} />
                    <Route path="/profile/:id" component={ProfileView} />
                    <Route path="*" component={PageNotFound} />
                </Switch>
            </div>
        );
    }
}
