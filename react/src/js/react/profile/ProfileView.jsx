import React from "react";

import ProfileHeaderView from "./ProfileHeaderView";
import ProfileStreamView from "./ProfileStreamView";

/**
 * Renders the view of a user's profile
 */
export default (props) => {
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