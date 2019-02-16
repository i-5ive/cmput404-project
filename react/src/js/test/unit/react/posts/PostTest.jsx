import React from "react";
import { expect } from "chai";
import Post from "react/posts/Post";
import { shallow } from "enzyme";

describe("Post Tests", () => {
    it("renders via shallow", () => {
        const page = shallow(Post />);

        //expect(page.text()).to.contain("Page Not Found!");
    });

    it('renders without crashing via dom', () => {
      const div = document.createElement('div');
      ReactDOM.render(<Post />, div);
      ReactDOM.unmountComponentAtNode(div);
    });
});
