#ifndef ENTITY_H
#define ENTITY_H
//LIBRARY INCLUDES:
#include <cstddef>
#include <string>
#include <vector>
#include <map>
#include <boost/lexical_cast.hpp>
//USER INCLUDES:
#include "chameleon.h"
#include "base/physicalObject.h"
#include "base/drawnObject.h"
#include "base/rect.h"
namespace base {
	using namespace std;
	class entity : public base::physicalObject {
		friend class boost::serialization::access;
		public:
			entity(vector<int> *_coords, map<string, string> *_data=NULL, chameleon::event::manager *_manager=NULL, int _curLevel=0);
			virtual base::drawnObject *clone() {return this;}
			virtual string getType() {return "entity";}
			void moveup(bool down);
			void movedown(bool down);
			void moveleft(bool down);
			void moveright(bool down);
			virtual void attack(base::group<base::physicalObject> *allSprites);
			virtual void update(base::group<base::physicalObject> *allSprites);
			chameleon::event::manager *getManager() {return manager;}
			int getCurLevel() {return curLevel;}
			void setCurLevel(int _curLevel) {curLevel = _curLevel;}
			int getAttr(string key) {return (*attrs)[key];}
		protected:
			chameleon::event::manager *manager;
			int curLevel;
			map<string, int> *attrs;
		private:
			template<class Archive>
			void serialize(Archive &ar, const unsigned int version);
			int requestx;
			int requesty;
	};
}
#endif
