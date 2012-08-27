#include "base/group.h"
using namespace std;
template<class T>
base::group<T>::group() {}
template<class T>
base::group<T>::group(base::group<T> *copy) : intern(new list<T *>(copy->intern)) {}
template<class T>
base::group<T>::~group() {delete intern;}
template<class T>
void base::group<T>::add(T *object) {
	intern->push_back(object);
}
template<class T>
void base::group<T>::remove(T *object) {
	intern->remove(object);
}
template<class T>
list<T *> *base::group<T>::getList() {
	return new list<T *>(*intern);
}
template<class T>
template<class Archive>
void base::group<T>::serialize(Archive &ar, const unsigned int version) {
	ar & intern;
}
