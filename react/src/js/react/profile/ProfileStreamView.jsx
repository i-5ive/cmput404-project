import React from "react";

import { Tabs, Tab, Thumbnail } from "react-bootstrap";

import PropTypes from "prop-types";

import ProfilePostsStream from "./ProfilePostsStream";
import ProfileFriendsList from "./ProfileFriendsList";

const ProfileStreamView = (props) => {
    return (
        <Thumbnail>
            <Tabs defaultActiveKey="posts" id="profile-stream-tabs">
                <Tab eventKey="posts" title="Posts">
                    <ProfilePostsStream id={props.id} />
                </Tab>
                <Tab eventKey="friends" title="Friends">
                    <ProfileFriendsList />
                </Tab>
            </Tabs>
        </Thumbnail>
    );
};

ProfileStreamView.propTypes = {
    id: PropTypes.string
};

export default ProfileStreamView;
