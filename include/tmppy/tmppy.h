/*
 * Copyright 2017 Google Inc. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef TMPPY_H
#define TMPPY_H

template <typename... Ts>
struct List;

template <bool... Ts>
struct BoolList;

template <bool>
struct AlwaysTrueFromBool {
  static constexpr bool value = true;
};

template <typename>
struct AlwaysTrueFromType {
  static constexpr bool value = true;
};

#endif // TMPPY_H
