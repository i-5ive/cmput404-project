import React from "react";
import { expect } from "chai";
import PostFeed from "react/posts/PostFeed";
import { shallow } from "enzyme";

describe("PostFeed Tests", () => {
    it("renders via shallow", () => {
        const page = shallow(<PostFeed />);

        //expect(page.text()).to.contain("Page Not Found!");
    });

    it('renders without crashing via dom', () => {
      const div = document.createElement('div');
      ReactDOM.render(<PostFeed />, div);
      ReactDOM.unmountComponentAtNode(div);
    });
});
