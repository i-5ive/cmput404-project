import React from "react";

import PropTypes from "prop-types";

import ProfileHeaderView from "./ProfileHeaderView";
import ProfileStreamView from "./ProfileStreamView";

/**
 * Renders the view of a user's profile
 */
const ProfileView = (props) => {
    const id = props.match.params.id;
    return (
        <div>
            <div className="profileHeader">
                <ProfileHeaderView id={id} />
            </div>
            <div className="profileStreamTabs">
                <ProfileStreamView id={id} />
            </div>
        </div>
    );
};

ProfileView.propTypes = {
    match: PropTypes.object
};

export default ProfileView;
