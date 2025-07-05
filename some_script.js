/**
 * Represents a person with a name and age.
 * @class
 * @property {string} name - The person's name. 
 * @property {number} age - The person's age.
 */
class Person {
    /**
     * Creates a new Person.
     * @param {string} name - The person's name.
     * @param {number} age - The person's age.
     */
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }

    /**
     * Returns a greeting message with the person's name and age.
     * @returns {string} The greeting message.
     */
    greet() {
        return `Hello, my name is ${this.name} and I am ${this.age} years old.`;
    }
}
