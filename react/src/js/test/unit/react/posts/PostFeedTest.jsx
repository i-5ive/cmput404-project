import React from "react";
import { expect } from "chai";
import PostFeed from "react/posts/PostFeed";
import Post from "react/posts/Post";
import { shallow } from "enzyme";

describe("PostFeed Tests", () => {
    it("renders via shallow", () => {
        const page = shallow(<PostFeed />);

        expect(page.contains(<Post/>));
    });
});
