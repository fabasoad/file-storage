import React from 'react';
import { shallow } from 'enzyme';
import File from '../../components/File';

let wrapper, expectedFileName, expectedCount, handleDeleteFile;

beforeEach(() => {
    expectedFileName = 'testFileName';
    expectedCount = 12;
    handleDeleteFile = jest.fn();
    wrapper = shallow(<File
        key={expectedFileName}
        fileName={expectedFileName}
        count={expectedCount}
        handleDeleteFile={handleDeleteFile}
    />);
});

test('should render File correctly', () => {
    expect(wrapper).toMatchSnapshot();
});

test('should handle handleDeleteFile', () => {
    wrapper.find('button').prop('onClick')();
    expect(handleDeleteFile).toHaveBeenLastCalledWith(expectedFileName);
});