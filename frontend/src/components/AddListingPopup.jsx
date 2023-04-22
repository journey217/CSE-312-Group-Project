import React, { useState, useEffect } from 'react';

function AddListingPopup({ onClose, onSubmit }) {
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [description, setDescription] = useState('');
  const [condition, setCondition] = useState('');
  const [date, setDate] = useState('');
  const [image, setImage] = useState(null);
  const [addListEnable, setAddListEnable] = useState(true);
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    if (name.trim() !== '' && price.trim() !== '' && description.trim() !== '' && condition.trim() !== '' && date.trim() !== '' && image !== null) {
      setAddListEnable(false);
    } else {
      setAddListEnable(true);
    }
    console.log(addListEnable)
  }, [name, price, description, condition, date, image]);

  const handleNameChange = (event) => {
    setName(event.target.value);
  };

  const handlePriceChange = (event) => {
    setPrice(event.target.value);
  };

  const handleDescriptionChange = (event) => {
    setDescription(event.target.value);
  };

  const handleConditionChange = (event) => {
    setCondition(event.target.value);
  };

  const handleImageChange = (event) => {
    setImage(event.target.files[0]);
  };

  const handleDateChange = (event) => {
    setDate(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);
    formData.append('Item_Name', name);
    formData.append('Item_Price', price);
    formData.append('Item_Desc', description);
    formData.append('condition', condition);
    formData.append('date', date);
    formData.append('image', image);

    fetch('/add-item', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        if (data.errors) {
          setErrors(data.errors);
          setSuccess(false);
        } else {
          setErrors({});
          setSuccess(true);
        }
      })
      .catch(error => console.error(error));
      onClose()
  };

  return (
    <div className="add-listing-popup">
      <h2>Add Listing</h2>
      {/*<form action="/add-item" method="POST" onSubmit={handleSubmit} encType="multipart/form-data">*/}
      <form onSubmit={handleSubmit}>
        <div className="form-field">
          {errors.field && <div className="error-message">{errors.field}</div>}
          <br />
          <label>Item Name:</label>
          <input name="Item_Name" type="text" value={name} onChange={handleNameChange} />
        </div>
        <div className="form-field">
          <label>Base Price:</label>
          <input name="Item_Price" type="number" value={price} onChange={handlePriceChange} />
        </div>
        <div className="form-field">
          <label>Description:</label>
          <textarea name="Item_Desc" value={description} onChange={handleDescriptionChange} />
        </div>
        <div className="form-field">
          <label>Condition:</label>
          <select name="condition" value={condition} onChange={handleConditionChange}>
            <option value="" disabled hidden>--- Select From Below ---</option>
            <option name="condition" value="Brand New">Brand New</option>
            <option name="condition" value="Like New">Like New</option>
            <option name="condition" value="Very Good">Very Good</option>
            <option name="condition" value="Good">Good</option>
            <option name="condition" value="Fair">Fair</option>
            <option name="condition" value="Poor">Poor</option>
          </select>
        </div>
        <div className="form-field">
          <label>Auction End Date:</label>
          <input name="date" value={date} type="date" onChange={handleDateChange} />
        </div>
        <div className="form-field">
          <label>Image:</label>
          <input name="image" type="file" onChange={handleImageChange} />
        </div>
        <button type="submit" disabled={addListEnable}>Add Listing</button>
        <button type="button" onClick={onClose}>Cancel</button>
        {success && <div>Item Listing Success!</div>}
      </form>
    </div>
  );
}

export default AddListingPopup;
