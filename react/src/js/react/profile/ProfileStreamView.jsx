import React from "react";

import { Tabs, Tab } from "react-bootstrap";

import ProfileGithubStream from "./ProfileGithubStream";
import ProfilePostsStream from "./ProfilePostsStream";

export default (props) => {
    return (
        <Tabs defaultActiveKey="posts" id="profile-stream-tabs">
            <Tab eventKey="posts" title="Posts">
                <ProfilePostsStream id={props.id} />
            </Tab>
            <Tab eventKey="github" title="Github">
                <ProfileGithubStream />
            </Tab>
        </Tabs>
    );
};