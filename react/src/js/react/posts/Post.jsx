import React from "react";

export default class Post extends React.Component {
    render() {
        return (
            <div className={this.props.className}>
                <h1>{this.props.className}</h1>
            </div>
        );
    }
}
