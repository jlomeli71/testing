/** Represents a person
 * @constructor
 * @param {string} name - The name of the person
 * @param {number} age - The age of the person
  */
 class Person {
    constructor(name, age) {
      this.name = name;
      this.age = age;
    }
    /**Greets with this person's name and age.
     * @returns {string} The greeting
    */
   greet()  {
    return `Hello, my name is ${this.name} and I am ${this.age} years old.`;
   }
  }
