import { MODALS } from 'cconstants';
import { useState } from 'react';
import { createRoot } from "react-dom/client";

import GenericModal from 'components/modals/Generic';
import { get_default_headers } from 'utils/fetcher';
import { User } from './types';

type Args = {
  onCancel: () => void;
  onOK: (user_id: string) => void;
  user: User;
}


async function api_delete_user(url: string, signal: AbortSignal): Promise<string|Response> {
  return fetch(
    url, {
      method: "delete",
      headers: get_default_headers(),
      signal: signal
    }
  );
}

const DeleteUserModal = ({onOK, onCancel, user}: Args) => {
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (signal: AbortSignal) => {
    let response = await api_delete_user(`/api/users/${user.id}`, signal);
    onOK(user.id);
  }

  const handleCancel = () => {
    setErrorMessage('');

    onCancel();
  }

  return (
    <GenericModal
      modal_title='Delete User'
      submit_button_title='Yes, delete user and all its documents'
      submit_button_variant='danger'
      onSubmit={handleSubmit}
      onCancel={handleCancel}>
        <p>
          Are you sure you want to delete user <b>{user.username}</b> and ALL his/her documents?
        </p>
    </GenericModal>
  );
}

function delete_user(user: User) {
  let modals = document.getElementById(MODALS);

  let promise = new Promise<string>(function(onOK, onCancel){
    if (modals) {
      let dom_root = createRoot(modals);

      dom_root.render(
        <DeleteUserModal
          user={user}
          onOK={onOK}
          onCancel={onCancel} />
      );
    }
  }); // new Promise...

  return promise;
}

export default delete_user;
