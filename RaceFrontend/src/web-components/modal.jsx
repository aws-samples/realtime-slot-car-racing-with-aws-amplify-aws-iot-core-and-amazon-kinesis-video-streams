import React from 'react'
import { Heading, View } from '@aws-amplify/ui-react';


const Modal = ({ handleClose, visible, title, children }) => {
  return (
    <>
      {visible &&
        <>
          <div className="overlay"></div>
          <View
            backgroundColor="var(--amplify-colors-white)"
            borderRadius="6px"
            border="2px solid var(--amplify-colors-white)"
            className="modal"
          >
            <header className="modal__header">
              <Heading style={{marginTop: '15px'}} level={3}>{title}</Heading>
              <button onClick={handleClose} className="close-button">&times;</button>
            </header>
            <main className="modal__main">
              { children }
            </main>
          </View>
        </>
      }
    </>
  );
};

export default Modal