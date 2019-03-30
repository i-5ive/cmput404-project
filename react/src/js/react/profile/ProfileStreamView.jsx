import React from "react";

import { Tabs, Tab, Thumbnail } from "react-bootstrap";

import PropTypes from "prop-types";

import ProfilePostsStream from "./ProfilePostsStream";
import ProfileFriendsList from "./ProfileFriendsList";
import ProfileFollowedUsers from "./ProfileFollowedUsers";
import ProfileFollowerUsers from "./ProfileFollowerUsers";

const ProfileStreamView = (props) => {
    return (
        <Thumbnail className="profile-stream">
            <Tabs defaultActiveKey="posts" id="profile-stream-tabs">
                <Tab eventKey="posts" title="Posts">
                    <ProfilePostsStream id={props.id} />
                </Tab>
                <Tab eventKey="friends" title="Friends">
                    <ProfileFriendsList />
                </Tab>
                <Tab eventKey="followed" title="Following">
                    <ProfileFollowedUsers id={props.id} />
                </Tab>
                <Tab eventKey="followers" title="Followers">
                    <ProfileFollowerUsers id={props.id} />
                </Tab>
            </Tabs>
        </Thumbnail>
    );
};

ProfileStreamView.propTypes = {
    id: PropTypes.string
};

export default ProfileStreamView;
