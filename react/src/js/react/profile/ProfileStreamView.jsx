import React from "react";

import { Tabs, Tab } from "react-bootstrap";

import PropTypes from "prop-types";

import ProfileGithubStream from "./ProfileGithubStream";
import ProfilePostsStream from "./ProfilePostsStream";

const ProfileStreamView = (props) => {
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

ProfileStreamView.propTypes = {
    id: PropTypes.string
};

export default ProfileStreamView;
